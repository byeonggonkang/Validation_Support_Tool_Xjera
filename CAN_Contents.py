diag_req_id = 0x74A
diab_res_id = 0x75A
CGW_TCU_G = 0x301
MFS_3 = 0x323
MFS_4 = 0x325
CGW_SAM_G = 0x340
CGW_EPS_G = 0x380
CEM_BCM_2 = 0x392
PLG = 0x436
NWM_CGW = 0x600
NWM_IHU = 0x618

#DIAGNOSTICS
diagusbDisable = [0x07, 0x2E, 0xF1, 0x01, 0x20, 0x10, 0x30, 0x02]
diagusbEnable = [0x07, 0x2E, 0xF1, 0x01, 0x20, 0x10, 0x30, 0x01]
diagExtendedSession = [0x02, 0x10, 0x03]
diagkeyReq = [0x02, 0x27, 0x03]
diagkeysend = [0x04, 0x27, 0x04, 0xfd, 0x6c]
diagconfigwrite = [0x23, 0x2e, 0xd0, 0x09, 0xa4, 0x01, 0xae, 0x90, 0x50, 0x0c, 0x00, 0x34, 0x13, 0x30, 0x08, 0x00, 0x87, 0x68, 0x40, 0x74, 0x00, 0x1c, 0x00, 0x01, 0x80, 0x01, 0x80, 0x02, 0x10, 0x01, 0xe1, 0x0b, 0xc0, 0x01, 0x00, 0x00]
diagVinwrite = [0x14, 0x2e, 0xf1, 0x90, 0x45, 0x43, 0x33, 0x44, 0x4c, 0x55, 0x47, 0x44, 0x35, 0x52, 0x30, 0x30, 0x30, 0x30, 0x32, 0x30, 0x37]
diagreset = [0x02, 0x11, 0x01]

#CGW_TCU_G
Gear_0 = [0x00, 0x00, 0x00, 0x00]
Gear_1 = [0x00, 0x04, 0x00, 0x00]
Gear_2 = [0x00, 0x08, 0x00, 0x00]
Gear_3 = [0x00, 0x0C, 0x00, 0x00]
Gear_4 = [0x00, 0x10, 0x00, 0x00]
Gear_5 = [0x00, 0x14, 0x00, 0x00]
Gear_6 = [0x00, 0x18, 0x00, 0x00]
Gear_7 = [0x00, 0x1C, 0x00, 0x00]
Gear_8 = [0x00, 0x20, 0x00, 0x00]

#MFS_3 for x70
MFS_WEchat_Press = [0x00, 0x10, 0x00, 0x00, 0x00, 0x00]
MFS_WEchat_Release = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

#MFS_3 for x50
MFS_3_L_UP_SW_Press = [0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
MFS_3_L_UP_SW_Release = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

MFS_3_L_DW_SW_Press = [0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
MFS_3_L_DW_SW_Release = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

MFS_3_L_LEFT_SW_Press = [0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
MFS_3_L_LEFT_SW_Release = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

MFS_3_L_RIGHT_SW_Press = [0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
MFS_3_L_RIGHT_SW_Release = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

MFS_3_L_OK_SW_Press = [0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
MFS_3_L_OK_SW_Release = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

MFS_3_L_WECHAT_SW_Press = [0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
MFS_3_L_WECHAT_SW_Release = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

MFS_3_L_USER_SW_Press = [0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
MFS_3_L_USER_SW_Release = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

MFS_3_R_UP_SW_Press = [0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
MFS_3_R_UP_SW_Release = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

MFS_3_R_DW_SW_Press = [0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00]
MFS_3_R_DW_SW_Release = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

MFS_3_R_LEFT_SW_Press = [0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00]
MFS_3_R_LEFT_SW_Release = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

MFS_3_R_RIGHT_SW_Press = [0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00]
MFS_3_R_RIGHT_SW_Release = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

MFS_3_R_OK_SW_Press = [0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00]
MFS_3_R_OK_SW_Release = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

MFS_3_R_RETURN_SW_Press = [0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00]
MFS_3_R_RETURN_SW_Release = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

MFS_3_R_SPEECH_SW_Press = [0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00]
MFS_3_R_SPEECH_SW_Release = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

#MFS_4 for x70
MFS_Menu_Press = [0x04, 0x00, 0x00, 0x00, 0x00, 0x00]
MFS_Menu_Release = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
MFS_LEFT_UP_Press = [0x10, 0x00, 0x00, 0x00, 0x00, 0x00]
MFS_LEFT_UP_Release = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
MFS_LEFT_DOWN_Press = [0x40, 0x00, 0x00, 0x00, 0x00, 0x00]
MFS_LEFT_DOWN_Release = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
MFS_LEFT_LEFT_Press = [0x00, 0x01, 0x00, 0x00, 0x00, 0x00]
MFS_LEFT_LEFT_Release = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
MFS_LEFT_RIGHT_Press = [0x00, 0x04, 0x00, 0x00, 0x00, 0x00]
MFS_LEFT_RIGHT_Release = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
MFS_Confirm_Press = [0x00, 0x10, 0x00, 0x00, 0x00, 0x00]
MFS_Confirm_Release = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
MFS_Mute_Press = [0x00, 0x00, 0x04, 0x00, 0x00, 0x00]
MFS_Mute_Release = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
MFS_Voice_Press = [0x00, 0x00, 0x10, 0x00, 0x00, 0x00]
MFS_Voice_Release = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
MFS_Voice_ADD_Press = [0x00, 0x00, 0x00, 0x04, 0x00, 0x00]
MFS_Voice_ADD_Release = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
MFS_Voice_Jian_Press = [0x00, 0x00, 0x00, 0x20, 0x00, 0x00]
MFS_Voice_Jian_Release = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
MFS_AnswerHangupPhone_Press = [0x00, 0x00, 0x00, 0x00, 0x01, 0x00]
MFS_AnswerHangupPhone_Release = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
MFS_Previous_Press = [0x00, 0x00, 0x00, 0x00, 0x04, 0x00]
MFS_Previous_Release = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
MFS_NEXT_Press = [0x00, 0x00, 0x00, 0x00, 0x10, 0x00]
MFS_NEXT_Release = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

#CGW_SAM_G
SteeringAngle0degree = [0x7F, 0xFD, 0xBE, 0x03, 0x00, 0x00, 0x00, 0x00]
SteeringAngle120degree = [0x87, 0x80, 0xBE, 0x03, 0x00, 0x00, 0x00, 0x00]
SteeringAnglem120degree = [0x78, 0x80, 0xBE, 0x03, 0x00, 0x00, 0x00, 0x00]

#CEM_BCM_2
DriverDoor_Open = [0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00]
DriverDoor_Close = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
AlarmMode_On = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01]
AlarmMode_Off = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
KeySts_Off = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
KeySts_On = [0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

#PLG
PLGSASSts_0 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
PLGSASSts_52 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x34, 0x00, 0x00]
PLGSASSts_100 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x64, 0x00, 0x00]
PLGSASSts_150 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x96, 0x00, 0x00]

#NWM_CGW
NM_WAKEUP_0 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
NM_WAKEUP_1 = [0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
NM_WAKEUP_2 = [0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
NM_WAKEUP_3 = [0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]