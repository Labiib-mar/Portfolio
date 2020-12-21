'''
Created Sept 17, 2019

@author: xxxxxxxx
Name: Labiib Ahmad Marzuki
E-mail: labiib.marzuki@gmail.com

Automatic Record of OEU report form OEU Loadeer.
This works for daily record only

'''

import cx_Oracle
import csv
import logging
import os
import time
import datetime
import tailer


'''
this sectionis for backup purposes only
used in case server or other technicals issue with the program scheduler
uncomment the line bellow and input desired date manually and run program
'''
#pastdate = datetime.datetime.strptime('1/2/2019', "%m/%d/%Y") # format is mm/dd/yyyy
#today = '9/10/2019' # format is mm/dd/yyyy


today = datetime.date.today()
#yesterday = today - datetime.timedelta(1)
#d1 ="\'"+yesterday.strftime('%m/%d/%Y')+"\'"
start_time = time.time()
dev_link = r'C:\Users\xxxxxxxx\Desktop\teeet\OEU_report.csv'
#prod_link = r'\\dkls16\Spotfire\OEU_Report\OEU_report.csv'
log_dev_link = r'C:\Users\xxxxxxxx\Desktop\teeet\log_OEU_report.csv'
#log_prod_link = r'\\dkls16\Spotfire\OEU_Report\log_OEU_report.csv'
    
output = open(dev_link,newline='')
a=tailer.tail(output,1)
b=a[0].split(',')
pastdate= datetime.datetime.strptime(b[0], "%Y-%m-%d %H:%M:%S")

try:

    while(pastdate!=today):
    #Connection to database please update the password area when necessary
        yesterday = pastdate - datetime.timedelta(1)
        d1 ="\'"+yesterday.strftime('%m/%d/%Y')+"\'"
        connection =cx_Oracle.connect('xxxxxxxxxxxxxxxxxxxxxxxxxxx')
        cursor = connection.cursor()
        query_qsheet = ("""
        select t3.*, Case When(t3."MTBA ERRORS" <> 0) Then round(t3."Production Time" / t3."MTBA ERRORS" ,2) Else round(t3."Production Time" / 1 ,2) End as "MTBA"  from
        (Select t1.*,
                       t2.DET,
                       t2.EFO,
                       t2."INDEX",
                       t2.NSOL,
                       t2.NSOP,
                       t2.SHTL,
                       t2.MC_OTHERS,
                       t2."MTBA ERRORS" from
                       (select a1.DTTM as "Date", a1.EQUIP as "Equipment", a1.LINE_GRP as "Module", a1.MODEL as "Technology",
        coalesce(Round((Sum(a1."Production Time"))/24*100,2),0) as "PROD%",
        coalesce(Round((Sum(a1."STBY")/24*100),2),0) as "STBY%",
        coalesce(Round((Sum(a1."ENGR")/24*100),2),0) as "ENGR%",
        coalesce(Round((coalesce(Sum(a1."UDWN"),0)+coalesce(Sum(a1.SDWN),0))/24*100,2),0) as "DOWN%",
        coalesce(Round((Sum(a1."NSCH")/24*100),2),0) as "NSCH%",
        coalesce(Round((Sum(a1."OFFL")/24*100),2),0) as "UDET%",
        coalesce(Round(Sum(a1."Production Time"),2),0) as "Production Time"
        from
        (select c1.DTTM,c1.EQUIP, c2.LINE_GRP, c2.MODEL,
        case when(proc_state='PROD') then sum(state_time) end as "Production Time",
        case when(proc_state='UDWN') then sum(state_time) end as "UDWN",
        case when(proc_state='SDWN') then sum(state_time) end as "SDWN",
        case when(proc_state='STBY') then sum(state_time) end as "STBY",
        case when(proc_state='ENGR') then sum(state_time) end as "ENGR",
        case when(proc_state='OFFL') then sum(state_time) end as "OFFL",
        case when(proc_state='NSCH') then sum(state_time) end as "NSCH"  
        from ASSY_OEU.EQUIP_PROCSTATE_DAILY c1, ASSY_OEU.EQUIP c2
        Where c1.facility=c2.facility
        and c1.equip=c2.equip
        and c1.facility='MLA'
        and c2.Process='WB'
        Group by c1.DTTM, c1.EQUIP, c1.PROC_STATE, c2.line_grp, c2.Model)a1
        group by a1.DTTM, a1.EQUIP, a1.LINE_GRP, a1.MODEL) t1
                  Left Join (Select b1.DTTM,
                                    b1.EQUIP,
                                    coalesce(Sum(b1.DET),0) AS DET,
                                    coalesce(Sum(b1.EFO),0) As EFO,
                                    coalesce(Sum(b1."INDEX"),0) As "INDEX",
                                    coalesce(Sum(b1.NSOL),0) As NSOL,
                                    coalesce(Sum(b1.NSOP),0) As NSOP,
                                    coalesce(Sum(b1.SHTL),0) As SHTL,
                                    coalesce(Sum(b1.MC_OTHERS),0) As MC_OTHERS,
                                    coalesce(Sum(b1."MTBA ERRORS"),0) As "MTBA ERRORS"
                               From (Select a2.FACILITY,
                                            a2.DTTM,
                                            a2.EQUIP,
                                            a2."Module",
                                            a2."Technology",
                                            Case
                                              When a2.ALTX_SYN = 'DET' Then
                                               Sum(a2.ALARM_COUNT_NET)
                                            End As DET,
                                            Case
                                              When a2.ALTX_SYN = 'EFO' Then
                                               Sum(a2.ALARM_COUNT_NET)
                                            End As EFO,
                                            Case
                                              When a2.ALTX_SYN = 'INDEX' Then
                                               Sum(a2.ALARM_COUNT_NET)
                                            End As "INDEX",
                                            Case
                                              When a2.ALTX_SYN = 'NSOL' Then
                                               Sum(a2.ALARM_COUNT_NET)
                                            End As NSOL,
                                            Case
                                              When a2.ALTX_SYN = 'NSOP' Then
                                               Sum(a2.ALARM_COUNT_NET)
                                            End As NSOP,
                                            Case
                                              When a2.ALTX_SYN = 'SHTL' Then
                                               Sum(a2.ALARM_COUNT_NET)
                                            End As SHTL,
                                            Case
                                              When a2.ALTX_SYN = '_MC_OTHERS' Then
                                               Sum(a2.ALARM_COUNT_NET)
                                            End As MC_OTHERS,
                                            Case
                                              When a2.ALTX_SYN = 'DET' Or a2.ALTX_SYN = 'EFO' Or
                                                   a2.ALTX_SYN = 'INDEX' Or
                                                   a2.ALTX_SYN = 'NSOL' Or
                                                   a2.ALTX_SYN = 'NSOP' Or
                                                   a2.ALTX_SYN = 'SHTL' Or
                                                   a2.ALTX_SYN = '_MC_OTHERS' Then
                                               Sum(a2.ALARM_COUNT_NET)
                                            End As "MTBA ERRORS"
                                       From (Select ASSY_OEU.EQUIP.FACILITY                    As FACILITY,
                                                    ASSY_OEU.EQUIP_ALARM_GRP.ALTX_SYN,
                                                    ASSY_OEU.EQUIP_ALARM_DAILY.ALID,
                                                    ASSY_OEU.EQUIP_ALARM_DAILY.DTTM,
                                                    ASSY_OEU.EQUIP_ALARM_DAILY.EQUIP,
                                                    ASSY_OEU.EQUIP_ALARM_DAILY.ALARM_COUNT,
                                                    ASSY_OEU.EQUIP_ALARM_DAILY.ALARM_TIME,
                                                    ASSY_OEU.EQUIP_ALARM_DAILY.ALARM_COUNT_NET,
                                                    ASSY_OEU.EQUIP.LINE_GRP                    As "Module",
                                                    ASSY_OEU.EQUIP.MODEL                       As "Technology"
                                               From ASSY_OEU.EQUIP_ALARM_GRP,
                                                    ASSY_OEU.EQUIP_ALARM_DAILY,
                                                    ASSY_OEU.EQUIP
                                              Where ASSY_OEU.EQUIP_ALARM_DAILY.FACILITY =
                                                    ASSY_OEU.EQUIP_ALARM_GRP.FACILITY
                                                And ASSY_OEU.EQUIP_ALARM_GRP.ALID =
                                                    ASSY_OEU.EQUIP_ALARM_DAILY.ALID
                                                And ASSY_OEU.EQUIP_ALARM_GRP.MODEL =
                                                    ASSY_OEU.EQUIP.MODEL
                                                And ASSY_OEU.EQUIP.EQUIP =
                                                    ASSY_OEU.EQUIP_ALARM_DAILY.EQUIP
                                                And ASSY_OEU.EQUIP.FACILITY = 'MLA'
                                                And ASSY_OEU.EQUIP.PROCESS = 'WB'
                                              Group By ASSY_OEU.EQUIP.FACILITY,
                                                       ASSY_OEU.EQUIP_ALARM_GRP.ALTX_SYN,
                                                       ASSY_OEU.EQUIP_ALARM_DAILY.ALID,
                                                       ASSY_OEU.EQUIP_ALARM_DAILY.DTTM,
                                                       ASSY_OEU.EQUIP_ALARM_DAILY.EQUIP,
                                                       ASSY_OEU.EQUIP_ALARM_DAILY.ALARM_COUNT,
                                                       ASSY_OEU.EQUIP_ALARM_DAILY.ALARM_TIME,
                                                       ASSY_OEU.EQUIP_ALARM_DAILY.ALARM_COUNT_NET,
                                                       ASSY_OEU.EQUIP.LINE_GRP,
                                                       ASSY_OEU.EQUIP.MODEL,
                                                       ASSY_OEU.EQUIP.PROCESS) a2
                                      Group By a2.FACILITY,
                                               a2.DTTM,
                                               a2.EQUIP,
                                               a2."Module",
                                               a2."Technology",
                                               a2.ALTX_SYN) b1
                              Group By b1.DTTM, b1.EQUIP) t2
                    On t1."Equipment" = t2.EQUIP And t1."Date" = t2.DTTM)t3
                   where t3."Date" = to_date("""+d1+""",'mm/dd/yyyy')
                   """)
        cursor.execute(query_qsheet)
        jobTime = time.time()
        #checkpoint file exists
        if not os.path.exists(dev_link):
            output = open(dev_link,"a",newline='')
            writer = csv.writer(output,delimiter=',')
            print ('Writing Data into file')
            writer.writerow([i[0] for i in cursor.description]) #write headers
            writer.writerows(cursor)
            print ('WB OEU report DATA GENERATION (create)--- Job Completed')
        else:
            output = open(dev_link,"a", newline='')
            writer = csv.writer(output,delimiter=',')
            print ('Writing Data into file. File existed. Appending new data')
            writer.writerows(cursor)
            print ('WB OEU report DATA GENERATION (append)--- Job Completed')
        pastdate = pastdate + datetime.timedelta(1)
    print (jobTime - start_time,"seconds")
    print("Done")

except:
    logging.basicConfig(filename=log_dev_link,filemode='a',format='%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S')
    log = logging.getLogger("ex")
    logging.error("Program Error!",exc_info=True)
    print('Error please refer to logfile')
