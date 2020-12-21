Select DDATE,
       EQUIPMENT,
       DET,
       EFO,
       IND,
       NSOL,
       NSOP,
       SHTL,
       MC_OTHERS,
       Coalesce(DET, 0) + Coalesce(EFO, 0) + Coalesce(IND, 0) +
       Coalesce(NSOL, 0) + Coalesce(NSOP, 0) + Coalesce(SHTL, 0) +
       Coalesce(MC_OTHERS, 0) As MTBA_OTHERS
  From (Select b.DDATE,
               b.EQUIPMENT,
               Sum(b.DET) As DET,
               Sum(b.EFO) As EFO,
               Sum(b.IND) As IND,
               Sum(b.NSOL) As NSOL,
               Sum(b.NSOP) As NSOP,
               Sum(b.SHTL) As SHTL,
               Sum(b.MC_OTHERS) As MC_OTHERS
          From (Select a.EQUIPMENT,
                       a.DDATE,
                       Case
                         When a.ERR_GRP = 'DET' Then
                          Sum(a.ALARM_COUNT_NET)
                       End As DET,
                       Case
                         When a.ERR_GRP = 'EFO' Then
                          Sum(a.ALARM_COUNT_NET)
                       End As EFO,
                       Case
                         When a.ERR_GRP = 'INDEX' Then
                          Sum(a.ALARM_COUNT_NET)
                       End As IND,
                       Case
                         When a.ERR_GRP = 'NSOL' Then
                          Sum(a.ALARM_COUNT_NET)
                       End As NSOL,
                       Case
                         When a.ERR_GRP = 'NSOP' Then
                          Sum(a.ALARM_COUNT_NET)
                       End As NSOP,
                       Case
                         When a.ERR_GRP = 'SHTL' Then
                          Sum(a.ALARM_COUNT_NET)
                       End As SHTL,
                       Case
                         When a.ERR_GRP = '_MC_OTHERS' Then
                          Sum(a.ALARM_COUNT_NET)
                       End As MC_OTHERS
                  From (Select ASSY_OEU.EQUIP_ALARM_DAILY.FACILITY,
                               ASSY_OEU.EQUIP_ALARM_DAILY.DTTM            As DDATE,
                               ASSY_OEU.EQUIP_ALARM_DAILY.EQUIP           As EQUIPMENT,
                               ASSY_OEU.EQUIP_ALARM_DAILY.ALID,
                               ASSY_OEU.EQUIP_ALARM_GRP.ALTX_SYN          As ERR_GRP,
                               ASSY_OEU.EQUIP_ALARM_DAILY.ALARM_COUNT,
                               ASSY_OEU.EQUIP_ALARM_DAILY.ALARM_TIME,
                               ASSY_OEU.EQUIP_ALARM_DAILY.ALARM_COUNT_NET
                          From ASSY_OEU.EQUIP_ALARM_DAILY,
                               ASSY_OEU.EQUIP,
                               ASSY_OEU.EQUIP_ALARM_GRP
                         Where ASSY_OEU.EQUIP.EQUIP =
                               ASSY_OEU.EQUIP_ALARM_DAILY.EQUIP
                           And ASSY_OEU.EQUIP_ALARM_GRP.MODEL =
                               ASSY_OEU.EQUIP.MODEL
                           And ASSY_OEU.EQUIP_ALARM_GRP.ALID =
                               ASSY_OEU.EQUIP_ALARM_DAILY.ALID
                           And ASSY_OEU.EQUIP.FACILITY = 'MLA'
                           And ASSY_OEU.EQUIP.PROCESS = 'WB'
                           And ASSY_OEU.EQUIP.EQUIP = 'KLMC6B05'
                           And ASSY_OEU.EQUIP_ALARM_DAILY.DTTM =
                               To_Date('9/10/2019', 'mm/dd/yyyy')
                         Group By ASSY_OEU.EQUIP_ALARM_DAILY.FACILITY,
                                  ASSY_OEU.EQUIP_ALARM_DAILY.DTTM,
                                  ASSY_OEU.EQUIP_ALARM_DAILY.EQUIP,
                                  ASSY_OEU.EQUIP_ALARM_DAILY.ALID,
                                  ASSY_OEU.EQUIP_ALARM_GRP.ALTX_SYN,
                                  ASSY_OEU.EQUIP_ALARM_DAILY.ALARM_COUNT,
                                  ASSY_OEU.EQUIP_ALARM_DAILY.ALARM_TIME,
                                  ASSY_OEU.EQUIP_ALARM_DAILY.ALARM_COUNT_NET) a
                 Group By a.EQUIPMENT, a.DDATE, a.ERR_GRP) b
         Group By b.DDATE, b.EQUIPMENT)
