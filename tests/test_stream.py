'''
Created on 3 Oct 2020 

*** NB: must be saved in UTF-8 format ***

Stream method tests for pyubx2.UBXReader

@author: semuadmin
'''

import os
import unittest

import pyubx2


class StreamTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        dirname = os.path.dirname(__file__)
        NAVLOG = os.path.join(dirname, 'pygpsdata-NAV.log')
        self.streamNAV = open(NAVLOG, 'rb')

    def tearDown(self):
        self.streamNAV.close()

    def testNAV(self):
        EXPECTED_RESULTS = (
        "<UBX(NAV-SOL, iTOW=14:04:51, fTOW=-77264, week=2128, gpsFix=3, flags=b'\\xdd', ecefX=380363769, ecefY=-14880401, ecefZ=510064462, pAcc=2632, ecefVX=-13, ecefVY=-2, ecefVZ=-6, sAcc=114, pDOP=194, reserved1=2, numSV=10, reserved2=215776)>",
        "<UBX(NAV-PVT, iTOW=14:04:51, year=2020, month=10, day=20, hour=14, min=4, second=49, valid=b'7', tAcc=38, nano=-77262, fixType=3, flags=b'\\x01', flags2=b'\\n', numSV=10, lon=-22403544, lat=534507692, height=84862, hMSL=36378, hAcc=16719, vAcc=20330, velN=68, velE=-26, velD=131, gSpeed=73, headMot=16142809, sAcc=1139, headAcc=2991983, pDOP=194, reserved1=151580049408, headVeh=0, magDec=0, magAcc=0)>",
        "<UBX(NAV-SVINFO, iTOW=14:04:51, numCh=23, globalFlags=b'\\x04', reserved2=0, chn_01=2, svid_01=2, flags_01=b'\\r', quality_01=b'\\x07', cno_01=35, elev_01=47, azim_01=255, prRes_01=-134, chn_02=6, svid_02=4, flags_02=b'\\r', quality_02=b'\\x04', cno_02=18, elev_02=15, azim_02=70, prRes_02=734, chn_03=3, svid_03=5, flags_03=b'\\r', quality_03=b'\\x04', cno_03=22, elev_03=39, azim_03=295, prRes_03=-1203, chn_04=4, svid_04=6, flags_04=b'\\x0c', quality_04=b'\\x03', cno_04=13, elev_04=30, azim_04=194, prRes_04=43, chn_05=0, svid_05=7, flags_05=b'\\r', quality_05=b'\\x04', cno_05=12, elev_05=57, azim_05=135, prRes_05=317, chn_06=1, svid_06=9, flags_06=b'\\r', quality_06=b'\\x04', cno_06=19, elev_06=52, azim_06=73, prRes_06=1223, chn_07=20, svid_07=13, flags_07=b'\\x04', quality_07=b'\\x01', cno_07=0, elev_07=6, azim_07=244, prRes_07=0, chn_08=16, svid_08=16, flags_08=b'\\x04', quality_08=b'\\x01', cno_08=0, elev_08=14, azim_08=41, prRes_08=0, chn_09=21, svid_09=26, flags_09=b'\\x04', quality_09=b'\\x01', cno_09=0, elev_09=3, azim_09=11, prRes_09=0, chn_10=18, svid_10=29, flags_10=b'\\x04', quality_10=b'\\x04', cno_10=18, elev_10=13, azim_10=320, prRes_10=0, chn_11=15, svid_11=30, flags_11=b'\\x04', quality_11=b'\\x03', cno_11=13, elev_11=38, azim_11=174, prRes_11=0, chn_12=17, svid_12=120, flags_12=b'\\x14', quality_12=b'\\x01', cno_12=0, elev_12=28, azim_12=196, prRes_12=0, chn_13=19, svid_13=123, flags_13=b'\\x14', quality_13=b'\\x01', cno_13=0, elev_13=22, azim_13=140, prRes_13=0, chn_14=8, svid_14=136, flags_14=b'\\x14', quality_14=b'\\x01', cno_14=0, elev_14=29, azim_14=171, prRes_14=0, chn_15=12, svid_15=69, flags_15=b'\\r', quality_15=b'\\x04', cno_15=22, elev_15=29, azim_15=84, prRes_15=-832, chn_16=9, svid_16=70, flags_16=b'\\r', quality_16=b'\\x06', cno_16=26, elev_16=75, azim_16=347, prRes_16=-77, chn_17=11, svid_17=71, flags_17=b'\\r', quality_17=b'\\x04', cno_17=26, elev_17=30, azim_17=285, prRes_17=-521, chn_18=14, svid_18=78, flags_18=b'\\x04', quality_18=b'\\x01', cno_18=0, elev_18=10, azim_18=16, prRes_18=0, chn_19=10, svid_19=79, flags_19=b'\\r', quality_19=b'\\x05', cno_19=26, elev_19=42, azim_19=61, prRes_19=-177, chn_20=7, svid_20=80, flags_20=b'\\x04', quality_20=b'\\x01', cno_20=0, elev_20=33, azim_20=136, prRes_20=0, chn_21=13, svid_21=85, flags_21=b'\\r', quality_21=b'\\x04', cno_21=25, elev_21=24, azim_21=232, prRes_21=232, chn_22=5, svid_22=86, flags_22=b'\\x04', quality_22=b'\\x01', cno_22=0, elev_22=39, azim_22=290, prRes_22=0, chn_23=22, svid_23=87, flags_23=b'\\x04', quality_23=b'\\x01', cno_23=0, elev_23=7, azim_23=354, prRes_23=0)>",
        "<UBX(NAV-ORB, iTOW=14:04:51, version=1, numCh=54, reserved1=0, gnssId_01=GPS, svId_01=1, svFlag_01=b'\\x05', eph_01=b'\\x00', alm_01=b'1', otherOrb_01=b'\\x00', gnssId_02=GPS, svId_02=2, svFlag_02=b'\\r', eph_02=b'0', alm_02=b'1', otherOrb_02=b'\\x00', gnssId_03=GPS, svId_03=3, svFlag_03=b'\\x05', eph_03=b'\\x00', alm_03=b'1', otherOrb_03=b'\\x00', gnssId_04=GPS, svId_04=4, svFlag_04=b'\\x1d', eph_04=b'(', alm_04=b'1', otherOrb_04=b'\\x00', gnssId_05=GPS, svId_05=5, svFlag_05=b'\\r', eph_05=b'0', alm_05=b'1', otherOrb_05=b'\\x00', gnssId_06=GPS, svId_06=6, svFlag_06=b'\\x1d', eph_06=b'(', alm_06=b'1', otherOrb_06=b'\\x00', gnssId_07=GPS, svId_07=7, svFlag_07=b'\\x1d', eph_07=b'(', alm_07=b'1', otherOrb_07=b'\\x00', gnssId_08=GPS, svId_08=8, svFlag_08=b'\\x05', eph_08=b'\\x00', alm_08=b'1', otherOrb_08=b'\\x00', gnssId_09=GPS, svId_09=9, svFlag_09=b'\\x1d', eph_09=b'(', alm_09=b'1', otherOrb_09=b'\\x00', gnssId_10=GPS, svId_10=10, svFlag_10=b'\\x05', eph_10=b'\\x00', alm_10=b'1', otherOrb_10=b'\\x00', gnssId_11=GPS, svId_11=11, svFlag_11=b'\\x05', eph_11=b'\\x00', alm_11=b'0', otherOrb_11=b'\\x00', gnssId_12=GPS, svId_12=12, svFlag_12=b'\\x05', eph_12=b'\\x00', alm_12=b'0', otherOrb_12=b'\\x00', gnssId_13=GPS, svId_13=13, svFlag_13=b'\\r', eph_13=b'\\x00', alm_13=b'0', otherOrb_13=b'\\x00', gnssId_14=GPS, svId_14=15, svFlag_14=b'\\x05', eph_14=b'\\x00', alm_14=b'0', otherOrb_14=b'\\x00', gnssId_15=GPS, svId_15=16, svFlag_15=b'\\r', eph_15=b'\\x00', alm_15=b'0', otherOrb_15=b'\\x00', gnssId_16=GPS, svId_16=17, svFlag_16=b'\\x05', eph_16=b'\\x00', alm_16=b'1', otherOrb_16=b'\\x00', gnssId_17=GPS, svId_17=18, svFlag_17=b'\\x05', eph_17=b'\\x00', alm_17=b'0', otherOrb_17=b'\\x00', gnssId_18=GPS, svId_18=19, svFlag_18=b'\\x05', eph_18=b'\\x00', alm_18=b'0', otherOrb_18=b'\\x00', gnssId_19=GPS, svId_19=20, svFlag_19=b'\\x05', eph_19=b'\\x00', alm_19=b'0', otherOrb_19=b'\\x00', gnssId_20=GPS, svId_20=22, svFlag_20=b'\\x05', eph_20=b'\\x00', alm_20=b'1', otherOrb_20=b'\\x00', gnssId_21=GPS, svId_21=23, svFlag_21=b'\\x05', eph_21=b'\\x00', alm_21=b'1', otherOrb_21=b'\\x00', gnssId_22=GPS, svId_22=24, svFlag_22=b'\\x05', eph_22=b'\\x00', alm_22=b'1', otherOrb_22=b'\\x00', gnssId_23=GPS, svId_23=25, svFlag_23=b'\\x05', eph_23=b'\\x00', alm_23=b'1', otherOrb_23=b'\\x00', gnssId_24=GPS, svId_24=26, svFlag_24=b'\\t', eph_24=b'\\x00', alm_24=b'1', otherOrb_24=b'\\x00', gnssId_25=GPS, svId_25=27, svFlag_25=b'\\x05', eph_25=b'\\x00', alm_25=b'1', otherOrb_25=b'\\x00', gnssId_26=GPS, svId_26=28, svFlag_26=b'\\x05', eph_26=b'\\x00', alm_26=b'1', otherOrb_26=b'\\x00', gnssId_27=GPS, svId_27=29, svFlag_27=b'\\r', eph_27=b'\\x00', alm_27=b'1', otherOrb_27=b'\\x00', gnssId_28=GPS, svId_28=30, svFlag_28=b'\\r', eph_28=b'\\x00', alm_28=b'1', otherOrb_28=b'\\x00', gnssId_29=GPS, svId_29=31, svFlag_29=b'\\x05', eph_29=b'\\x00', alm_29=b'1', otherOrb_29=b'\\x00', gnssId_30=GPS, svId_30=32, svFlag_30=b'\\x05', eph_30=b'\\x00', alm_30=b'1', otherOrb_30=b'\\x00', gnssId_31=GLONASS, svId_31=1, svFlag_31=b'\\x05', eph_31=b'\\x00', alm_31=b'?', otherOrb_31=b'\\x00', gnssId_32=GLONASS, svId_32=2, svFlag_32=b'\\x05', eph_32=b'\\x00', alm_32=b'?', otherOrb_32=b'\\x00', gnssId_33=GLONASS, svId_33=3, svFlag_33=b'\\x05', eph_33=b'\\x00', alm_33=b'?', otherOrb_33=b'\\x00', gnssId_34=GLONASS, svId_34=4, svFlag_34=b'\\x05', eph_34=b'\\x00', alm_34=b'?', otherOrb_34=b'\\x00', gnssId_35=GLONASS, svId_35=5, svFlag_35=b'\\r', eph_35=b'?', alm_35=b'?', otherOrb_35=b'\\x00', gnssId_36=GLONASS, svId_36=6, svFlag_36=b'\\r', eph_36=b'?', alm_36=b'?', otherOrb_36=b'\\x00', gnssId_37=GLONASS, svId_37=7, svFlag_37=b'\\r', eph_37=b'?', alm_37=b'?', otherOrb_37=b'\\x00', gnssId_38=GLONASS, svId_38=8, svFlag_38=b'\\x05', eph_38=b'\\x00', alm_38=b'?', otherOrb_38=b'\\x00', gnssId_39=GLONASS, svId_39=9, svFlag_39=b'\\x05', eph_39=b'\\x00', alm_39=b'?', otherOrb_39=b'\\x00', gnssId_40=GLONASS, svId_40=10, svFlag_40=b'\\x05', eph_40=b'\\x00', alm_40=b'?', otherOrb_40=b'\\x00', gnssId_41=GLONASS, svId_41=11, svFlag_41=b'\\x05', eph_41=b'\\x00', alm_41=b'?', otherOrb_41=b'\\x00', gnssId_42=GLONASS, svId_42=12, svFlag_42=b'\\x05', eph_42=b'\\x00', alm_42=b'?', otherOrb_42=b'\\x00', gnssId_43=GLONASS, svId_43=13, svFlag_43=b'\\x05', eph_43=b'\\x00', alm_43=b'?', otherOrb_43=b'\\x00', gnssId_44=GLONASS, svId_44=14, svFlag_44=b'\\r', eph_44=b'\\x00', alm_44=b'?', otherOrb_44=b'\\x00', gnssId_45=GLONASS, svId_45=15, svFlag_45=b'\\r', eph_45=b'?', alm_45=b'?', otherOrb_45=b'\\x00', gnssId_46=GLONASS, svId_46=16, svFlag_46=b'\\r', eph_46=b'\\x00', alm_46=b'?', otherOrb_46=b'\\x00', gnssId_47=GLONASS, svId_47=17, svFlag_47=b'\\x05', eph_47=b'\\x00', alm_47=b'?', otherOrb_47=b'\\x00', gnssId_48=GLONASS, svId_48=18, svFlag_48=b'\\x05', eph_48=b'\\x00', alm_48=b'?', otherOrb_48=b'\\x00', gnssId_49=GLONASS, svId_49=19, svFlag_49=b'\\x05', eph_49=b'\\x00', alm_49=b'?', otherOrb_49=b'\\x00', gnssId_50=GLONASS, svId_50=20, svFlag_50=b'\\x05', eph_50=b'\\x00', alm_50=b'?', otherOrb_50=b'\\x00', gnssId_51=GLONASS, svId_51=21, svFlag_51=b'\\r', eph_51=b'?', alm_51=b'?', otherOrb_51=b'\\x00', gnssId_52=GLONASS, svId_52=22, svFlag_52=b'\\r', eph_52=b'\\x00', alm_52=b'?', otherOrb_52=b'\\x00', gnssId_53=GLONASS, svId_53=23, svFlag_53=b'\\r', eph_53=b'\\x00', alm_53=b'?', otherOrb_53=b'\\x00', gnssId_54=GLONASS, svId_54=24, svFlag_54=b'\\x05', eph_54=b'\\x00', alm_54=b'?', otherOrb_54=b'\\x00')>",
        "<UBX(NAV-SAT, iTOW=14:04:51, version=1, numCh=23, reserved11=0, reserved12=0, gnssId_01=GPS, svId_01=2, cno_01=35, elev_01=47, azim_01=255, prRes_01=-13, flags_01=b'\\x1f\\x19\\x00\\x00', gnssId_02=GPS, svId_02=4, cno_02=18, elev_02=15, azim_02=70, prRes_02=73, flags_02=b'\\x1c\\x19\\x00\\x00', gnssId_03=GPS, svId_03=5, cno_03=22, elev_03=39, azim_03=295, prRes_03=-120, flags_03=b'\\x1c\\x19\\x00\\x00', gnssId_04=GPS, svId_04=6, cno_04=13, elev_04=30, azim_04=194, prRes_04=4, flags_04=b'\\x13\\x19\\x00\\x00', gnssId_05=GPS, svId_05=7, cno_05=12, elev_05=57, azim_05=135, prRes_05=32, flags_05=b'\\x1c\\x19\\x00\\x00', gnssId_06=GPS, svId_06=9, cno_06=19, elev_06=52, azim_06=73, prRes_06=122, flags_06=b'\\x1c\\x19\\x00\\x00', gnssId_07=GPS, svId_07=13, cno_07=0, elev_07=6, azim_07=244, prRes_07=0, flags_07=b'\\x11\\x12\\x00\\x00', gnssId_08=GPS, svId_08=16, cno_08=0, elev_08=14, azim_08=41, prRes_08=0, flags_08=b'\\x11\\x12\\x00\\x00', gnssId_09=GPS, svId_09=26, cno_09=0, elev_09=3, azim_09=11, prRes_09=0, flags_09=b'\\x11\\x12\\x00\\x00', gnssId_10=GPS, svId_10=29, cno_10=18, elev_10=13, azim_10=320, prRes_10=0, flags_10=b'\\x14\\x12\\x00\\x00', gnssId_11=GPS, svId_11=30, cno_11=13, elev_11=38, azim_11=174, prRes_11=0, flags_11=b'\\x13\\x12\\x00\\x00', gnssId_12=SBAS, svId_12=120, cno_12=0, elev_12=28, azim_12=196, prRes_12=0, flags_12=b'\\x01\\x07\\x00\\x00', gnssId_13=SBAS, svId_13=123, cno_13=0, elev_13=22, azim_13=140, prRes_13=0, flags_13=b'\\x01\\x07\\x00\\x00', gnssId_14=SBAS, svId_14=136, cno_14=0, elev_14=29, azim_14=171, prRes_14=0, flags_14=b'\\x01\\x07\\x00\\x00', gnssId_15=GLONASS, svId_15=5, cno_15=22, elev_15=29, azim_15=84, prRes_15=-83, flags_15=b'\\x1c\\x19\\x00\\x00', gnssId_16=GLONASS, svId_16=6, cno_16=26, elev_16=75, azim_16=347, prRes_16=-8, flags_16=b'\\x1e\\x19\\x00\\x00', gnssId_17=GLONASS, svId_17=7, cno_17=26, elev_17=30, azim_17=285, prRes_17=-52, flags_17=b'\\x1c\\x19\\x00\\x00', gnssId_18=GLONASS, svId_18=14, cno_18=0, elev_18=10, azim_18=16, prRes_18=0, flags_18=b'\\x11\\x12\\x00\\x00', gnssId_19=GLONASS, svId_19=15, cno_19=26, elev_19=42, azim_19=61, prRes_19=-18, flags_19=b'\\x1d\\x19\\x00\\x00', gnssId_20=GLONASS, svId_20=16, cno_20=0, elev_20=33, azim_20=136, prRes_20=0, flags_20=b'\\x11\\x12\\x00\\x00', gnssId_21=GLONASS, svId_21=21, cno_21=25, elev_21=24, azim_21=232, prRes_21=23, flags_21=b'\\x1c\\x19\\x00\\x00', gnssId_22=GLONASS, svId_22=22, cno_22=0, elev_22=39, azim_22=290, prRes_22=0, flags_22=b'\\x11\\x12\\x00\\x00', gnssId_23=GLONASS, svId_23=23, cno_23=0, elev_23=7, azim_23=354, prRes_23=0, flags_23=b'\\x11\\x12\\x00\\x00')>",
        "<UBX(NAV-STATUS, iTOW=14:04:51, gpsFix=3, flags=b'\\xdd', fixStat=b'\\x00', flags2=b'\\x08', ttff=1882, msss=23382)>",
        "<UBX(NAV-POSECEF, iTOW=14:04:51, ecefX=380363769, ecefY=-14880401, ecefZ=510064462, pAcc=2632)>",
        "<UBX(NAV-POSLLH, iTOW=14:04:51, lon=-22403544, lat=534507692, height=84862, hMSL=36378, hAcc=16719, vAcc=20330)>",
        "<UBX(NAV-DOP, iTOW=14:04:51, gDOP=219, pDOP=194, tDOP=102, vDOP=154, hDOP=118, nDOP=107, eDOP=49)>",
        "<UBX(NAV-VELECEF, iTOW=14:04:51, ecefVX=-13, ecefVY=-2, ecefVZ=-6, sAcc=114)>",
        "<UBX(NAV-VELNED, iTOW=14:04:51, velN=7, velE=-3, velD=13, speed=15, gSpeed=7, heading=16142809, sAcc=114, cAcc=2991983)>",
        "<UBX(NAV-TIMEGPS, iTOW=14:04:51, fTOW=-77264, week=2128, leapS=18, valid=b'\\x07', tAcc=38)>",
        "<UBX(NAV-TIMEGLO, iTOW=14:04:51, TOD=61489, fTOD=-77299, Nt=294, N4=7, valid=b'\\x03', tAcc=41)>",
        "<UBX(NAV-TIMEBDS, iTOW=14:04:51, SOW=223493, fSOW=-77264, week=772, leapS=4, valid=b'\\x07', tAcc=3374)>",
        "<UBX(NAV-TIMEGAL, iTOW=14:04:51, galTow=223507, fGalTow=-77264, galWno=1104, leapS=18, valid=b'\\x07', tAcc=3374)>",
        "<UBX(NAV-TIMEUTC, iTOW=14:04:51, tAcc=38, nano=838860800, year=65234, month=255, day=228, hour=7, min=10, sec=20, validflags=b'\\x0e')>",
        "<UBX(NAV-TIMELS, iTOW=14:04:51, version=0, reserved1=0, srcOfCurrLs=2, currLs=18, srcOfLsChange=2, lsChange=0, timeToLsEvent=34854912, dateOfLsGpsWn=2185, dateOfLsGpsDn=7, reserved2=0, valid=b'\\x03')>",
        "<UBX(NAV-CLOCK, iTOW=14:04:51, clkB=77264, clkD=346, tAcc=38, fAcc=1902)>",
        "<UBX(NAV-SBAS, iTOW=14:04:51, geo=0, mode:=0, sys=0, service=b'\\x00', numCh=0, reserved0=0)>",
        "<UBX(NAV-DGPS, iTOW=14:04:51, age=0, baseId=0, baseHealth=0, numCh=0, status=0, reserved1=0)>",
        "<UBX(NAV-AOPSTATUS, iTOW=14:04:51, config=0, status=0, reserved0=0, reserved1=10, avail=0, reserved2=0, reserved3=0)>",
        "<UBX(NAV-ODO, version=0, reserved13=67, iTOW=04:17:36.641000, distance=3410, totalDistance=0, distanceStd=0)>",
        "<UBX(NAV-GEOFENCE, iTOW=14:04:51, version=0, status=0, numFences=0, combState=0)>",
        "<UBX(NAV-EOE, iTOW=14:04:51)>"
        )

        i = 0
        raw = 0
        ubxreader = pyubx2.UBXReader(self.streamNAV)
        print("\n")
        while raw is not None:
            (raw, parsed) = ubxreader.read()
            if raw is not None:
                print(f"Testing {str(parsed).split(',')[0][5:]}")
                self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                i += 1
        print("\n")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
