"""
Stream method tests for pyubx2.UBXReader

Created on 3 Oct 2020 

*** NB: must be saved in UTF-8 format ***

@author: semuadmin
"""
# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import os
import unittest

from pyubx2 import UBXReader, VALCKSUM
from pyubx2.exceptions import UBXStreamError


class StreamTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        dirname = os.path.dirname(__file__)
        self.streamINF = open(os.path.join(dirname, "pygpsdata-INF.log"), "rb")
        self.streamMON = open(os.path.join(dirname, "pygpsdata-MON.log"), "rb")
        self.streamRXM = open(os.path.join(dirname, "pygpsdata-RXM.log"), "rb")
        self.streamMIX = open(os.path.join(dirname, "pygpsdata-MIXED.log"), "rb")
        self.streamMIX2 = open(os.path.join(dirname, "pygpsdata-MIXED2.log"), "rb")
        self.streamHNR = open(os.path.join(dirname, "pygpsdata-HNR.log"), "rb")
        self.streamBADHDR = open(os.path.join(dirname, "pygpsdata-BADHDR.log"), "rb")
        self.streamBADEOF1 = open(os.path.join(dirname, "pygpsdata-BADEOF1.log"), "rb")
        self.streamBADEOF2 = open(os.path.join(dirname, "pygpsdata-BADEOF2.log"), "rb")
        self.streamBADEOF3 = open(os.path.join(dirname, "pygpsdata-BADEOF3.log"), "rb")
        self.esf_meas_log = [
            b"\xb5b\x10\x02\x18\x00\x72\xd8\x07\x00\x18\x18\x00\x00\x4b\xfd\xff\x10\x40\x02\x00\x11\x23\x28\x00\x12\x72\xd8\x07\x00\x03\x9c",
            b"\xb5b\x10\x02\x1c\x00\x6d\xd8\x07\x00\x18\x20\x00\x00\xcd\x06\x00\x0e\xe4\xfe\xff\x0d\x03\xfa\xff\x05\x09\x0b\x00\x0c\x6d\xd8\x07\x00\xee\x51",
            b"\xb5b\x10\x02\x18\x00\xd5\xd8\x07\x00\x18\x18\x00\x00\x4d\xfd\xff\x10\x45\x02\x00\x11\x1f\x28\x00\x12\xd5\xd8\x07\x00\xcc\xac",
            b"\xb5b\x10\x02\x1c\x00\xd0\xd8\x07\x00\x18\x20\x00\x00\x7c\x06\x00\x0e\xcb\xfe\xff\x0d\xac\xf9\xff\x05\x09\x0b\x00\x0c\xd0\xd8\x07\x00\xf2\xae",
            b"\xb5b\x10\x02\x18\x00\x38\xd9\x07\x00\x18\x18\x00\x00\x4a\xfd\xff\x10\x41\x02\x00\x11\x27\x28\x00\x12\x38\xd9\x07\x00\x95\x7a",
            b"\xb5b\x10\x02\x1c\x00\x33\xd9\x07\x00\x18\x20\x00\x00\x0f\x06\x00\x0e\x16\xfe\xff\x0d\x5b\xfa\xff\x05\x0a\x0b\x00\x0c\x33\xd9\x07\x00\x49\x9f",
            b"\xb5b\x10\x02\x18\x00\x9c\xd9\x07\x00\x18\x18\x00\x00\x4e\xfd\xff\x10\x4e\x02\x00\x11\x20\x28\x00\x12\x9c\xd9\x07\x00\x67\x0e",
            b"\xb5b\x10\x02\x1c\x00\x97\xd9\x07\x00\x18\x20\x00\x00\x85\x06\x00\x0e\x77\xfe\xff\x0d\xe1\xf9\xff\x05\x0a\x0b\x00\x0c\x97\xd9\x07\x00\x6d\xa4",
            b"\xb5b\x10\x02\x18\x00\xff\xd9\x07\x00\x18\x18\x00\x00\x4c\xfd\xff\x10\x3e\x02\x00\x11\x24\x28\x00\x12\xff\xd9\x07\x00\x1f\x22",
            b"\xb5b\x10\x02\x1c\x00\xfa\xd9\x07\x00\x18\x20\x00\x00\x92\x06\x00\x0e\x61\xfe\xff\x0d\x9f\xf9\xff\x05\x0a\x0b\x00\x0c\xfa\xd9\x07\x00\xe8\x90",
            b"\xb5b\x10\x02\x18\x00\x63\xda\x07\x00\x18\x18\x00\x00\x47\xfd\xff\x10\x44\x02\x00\x11\x1c\x28\x00\x12\x63\xda\x07\x00\xe2\xe4",
            b"\xb5b\x10\x02\x1c\x00\x5e\xda\x07\x00\x18\x20\x00\x00\xef\x06\x00\x0e\xb8\xfe\xff\x0d\xc8\xf9\xff\x05\x0a\x0b\x00\x0c\x5e\xda\x07\x00\x8f\xce",
            b"\xb5b\x10\x02\x18\x00\xc6\xda\x07\x00\x18\x18\x00\x00\x4a\xfd\xff\x10\x4e\x02\x00\x11\x21\x28\x00\x12\xc6\xda\x07\x00\xba\x88",
            b"\xb5b\x10\x02\x1c\x00\xc1\xda\x07\x00\x18\x20\x00\x00\x82\x06\x00\x0e\x5b\xfe\xff\x0d\xc8\xf9\xff\x05\x09\x0b\x00\x0c\xc1\xda\x07\x00\x8a\xd2",
            b"\xb5b\x10\x02\x18\x00\x2a\xdb\x07\x00\x18\x18\x00\x00\x48\xfd\xff\x10\x47\x02\x00\x11\x27\x28\x00\x12\x2a\xdb\x07\x00\x81\x4e",
            b"\xb5b\x10\x02\x1c\x00\x25\xdb\x07\x00\x18\x20\x00\x00\x1b\x07\x00\x0e\xed\xfe\xff\x0d\xfa\xf9\xff\x05\x09\x0b\x00\x0c\x25\xdb\x07\x00\xb2\xef",
            b"\xb5b\x10\x02\x1c\x00\xdb\x25\x01\x00\x18\x20\x00\x00\x76\x02\x00\x0e\x06\xf8\xff\x0d\xde\xf7\xff\x05\x54\x0a\x00\x0c\xdb\x25\x01\x00\x3b\x91",
            b"\xb5b\x10\x02\x18\x00\xee\x23\x01\x00\x18\x18\x00\x00\xe8\x11\x00\x10\xfa\x07\x00\x11\xa1\x22\x00\x12\xee\x23\x01\x00\x6e\xf9",
            b"\xb5b\x10\x02\x1c\x00\x94\x21\x01\x00\x18\x20\x00\x00\xff\x05\x00\x0e\xf3\xfe\xff\x0d\x4d\x0b\x00\x05\x51\x0a\x00\x0c\x94\x21\x01\x00\xa5\x52",
        ]

    def tearDown(self):
        self.streamINF.close()
        self.streamMON.close()
        self.streamRXM.close()
        self.streamMIX.close()
        self.streamMIX2.close()
        self.streamHNR.close()
        self.streamBADHDR.close()
        self.streamBADEOF1.close()
        self.streamBADEOF2.close()
        self.streamBADEOF3.close()

    def testMIX2(self):  # test mixed UBX/NMEA stream with validate set to False
        EXPECTED_RESULTS = (
            "<UBX(NAV-EOE, iTOW=09:08:04)>",
            "<UBX(NAV-PVT, iTOW=09:08:09, year=2021, month=2, day=22, hour=9, min=8, second=7, validDate=1, validTime=1, fullyResolved=1, validMag=0, tAcc=1071, nano=332985, fixType=3, gnssFixOk=1, difSoln=0, psmState=0, headVehValid=0, carrSoln=0, confirmedAvai=1, confirmedDate=0, confirmedTime=1, numSV=4, lon=-22401762, lat=534506799, height=72728, hMSL=24245, hAcc=55374, vAcc=35349, velN=362, velE=-50, velD=-71, gSpeed=365, headMot=0, sAcc=4508, headAcc=13597116, pDOP=520, reserved1=52016683286528, headVeh=0, magDec=0, magAcc=0)>",
            "<UBX(NAV-ORB, iTOW=09:08:09, version=1, numSv=33, reserved1=0, gnssId_01=GPS, svId_01=1, health_01=1, visibility_01=1, ephUsability_01=0, ephSource_01=0, almUsability_01=17, almSource_01=1, anoAopUsability_01=0, type_01=0, gnssId_02=GPS, svId_02=14, health_02=1, visibility_02=3, ephUsability_02=12, ephSource_02=1, almUsability_02=15, almSource_02=3, anoAopUsability_02=7, type_02=2, gnssId_03=GPS, svId_03=19, health_03=1, visibility_03=1, ephUsability_03=0, ephSource_03=0, almUsability_03=16, almSource_03=1, anoAopUsability_03=0, type_03=0, gnssId_04=GPS, svId_04=20, health_04=1, visibility_04=3, ephUsability_04=0, ephSource_04=0, almUsability_04=17, almSource_04=1, anoAopUsability_04=0, type_04=0, gnssId_05=GPS, svId_05=21, health_05=1, visibility_05=1, ephUsability_05=0, ephSource_05=0, almUsability_05=17, almSource_05=1, anoAopUsability_05=0, type_05=0, gnssId_06=GPS, svId_06=22, health_06=1, visibility_06=1, ephUsability_06=0, ephSource_06=0, almUsability_06=17, almSource_06=1, anoAopUsability_06=0, type_06=0, gnssId_07=GPS, svId_07=23, health_07=1, visibility_07=3, ephUsability_07=0, ephSource_07=0, almUsability_07=17, almSource_07=1, anoAopUsability_07=0, type_07=0, gnssId_08=GPS, svId_08=24, health_08=1, visibility_08=3, ephUsability_08=12, ephSource_08=1, almUsability_08=15, almSource_08=3, anoAopUsability_08=7, type_08=2, gnssId_09=GPS, svId_09=25, health_09=1, visibility_09=0, ephUsability_09=0, ephSource_09=0, almUsability_09=17, almSource_09=1, anoAopUsability_09=0, type_09=0, gnssId_10=GLONASS, svId_10=1, health_10=1, visibility_10=1, ephUsability_10=0, ephSource_10=0, almUsability_10=21, almSource_10=1, anoAopUsability_10=0, type_10=0, gnssId_11=GLONASS, svId_11=2, health_11=1, visibility_11=1, ephUsability_11=0, ephSource_11=0, almUsability_11=21, almSource_11=1, anoAopUsability_11=0, type_11=0, gnssId_12=GLONASS, svId_12=3, health_12=1, visibility_12=1, ephUsability_12=0, ephSource_12=0, almUsability_12=21, almSource_12=1, anoAopUsability_12=0, type_12=0, gnssId_13=GLONASS, svId_13=4, health_13=1, visibility_13=3, ephUsability_13=0, ephSource_13=0, almUsability_13=21, almSource_13=1, anoAopUsability_13=0, type_13=0, gnssId_14=GLONASS, svId_14=5, health_14=1, visibility_14=3, ephUsability_14=6, ephSource_14=1, almUsability_14=21, almSource_14=1, anoAopUsability_14=7, type_14=2, gnssId_15=GLONASS, svId_15=6, health_15=1, visibility_15=3, ephUsability_15=0, ephSource_15=0, almUsability_15=21, almSource_15=1, anoAopUsability_15=0, type_15=0, gnssId_16=GLONASS, svId_16=7, health_16=1, visibility_16=1, ephUsability_16=0, ephSource_16=0, almUsability_16=21, almSource_16=1, anoAopUsability_16=0, type_16=0, gnssId_17=GLONASS, svId_17=8, health_17=1, visibility_17=1, ephUsability_17=0, ephSource_17=0, almUsability_17=21, almSource_17=1, anoAopUsability_17=0, type_17=0, gnssId_18=GLONASS, svId_18=9, health_18=1, visibility_18=1, ephUsability_18=0, ephSource_18=0, almUsability_18=21, almSource_18=1, anoAopUsability_18=0, type_18=0, gnssId_19=GLONASS, svId_19=10, health_19=1, visibility_19=1, ephUsability_19=0, ephSource_19=0, almUsability_19=21, almSource_19=1, anoAopUsability_19=0, type_19=0, gnssId_20=GLONASS, svId_20=11, health_20=2, visibility_20=1, ephUsability_20=0, ephSource_20=0, almUsability_20=21, almSource_20=1, anoAopUsability_20=0, type_20=0, gnssId_21=GLONASS, svId_21=12, health_21=1, visibility_21=1, ephUsability_21=0, ephSource_21=0, almUsability_21=21, almSource_21=1, anoAopUsability_21=0, type_21=0, gnssId_22=GLONASS, svId_22=13, health_22=1, visibility_22=2, ephUsability_22=0, ephSource_22=0, almUsability_22=21, almSource_22=1, anoAopUsability_22=0, type_22=0, gnssId_23=GLONASS, svId_23=14, health_23=1, visibility_23=3, ephUsability_23=0, ephSource_23=0, almUsability_23=21, almSource_23=1, anoAopUsability_23=0, type_23=0, gnssId_24=GLONASS, svId_24=15, health_24=1, visibility_24=3, ephUsability_24=6, ephSource_24=1, almUsability_24=21, almSource_24=1, anoAopUsability_24=7, type_24=2, gnssId_25=GLONASS, svId_25=16, health_25=1, visibility_25=3, ephUsability_25=0, ephSource_25=0, almUsability_25=21, almSource_25=1, anoAopUsability_25=0, type_25=0, gnssId_26=GLONASS, svId_26=17, health_26=1, visibility_26=1, ephUsability_26=0, ephSource_26=0, almUsability_26=21, almSource_26=1, anoAopUsability_26=0, type_26=0, gnssId_27=GLONASS, svId_27=18, health_27=1, visibility_27=1, ephUsability_27=0, ephSource_27=0, almUsability_27=21, almSource_27=1, anoAopUsability_27=0, type_27=0, gnssId_28=GLONASS, svId_28=19, health_28=1, visibility_28=1, ephUsability_28=0, ephSource_28=0, almUsability_28=21, almSource_28=1, anoAopUsability_28=0, type_28=0, gnssId_29=GLONASS, svId_29=20, health_29=1, visibility_29=1, ephUsability_29=0, ephSource_29=0, almUsability_29=21, almSource_29=1, anoAopUsability_29=0, type_29=0, gnssId_30=GLONASS, svId_30=21, health_30=1, visibility_30=2, ephUsability_30=0, ephSource_30=0, almUsability_30=21, almSource_30=1, anoAopUsability_30=0, type_30=0, gnssId_31=GLONASS, svId_31=22, health_31=1, visibility_31=3, ephUsability_31=0, ephSource_31=0, almUsability_31=21, almSource_31=1, anoAopUsability_31=0, type_31=0, gnssId_32=GLONASS, svId_32=23, health_32=1, visibility_32=2, ephUsability_32=0, ephSource_32=0, almUsability_32=21, almSource_32=1, anoAopUsability_32=0, type_32=0, gnssId_33=GLONASS, svId_33=24, health_33=1, visibility_33=1, ephUsability_33=0, ephSource_33=0, almUsability_33=21, almSource_33=1, anoAopUsability_33=0, type_33=0)>",
            "<UBX(NAV-SAT, iTOW=09:08:09, version=1, numCh=19, reserved11=0, reserved12=0, gnssId_01=GPS, svId_01=3, cno_01=0, elev_01=-91, azim_01=0, prRes_01=0, qualityInd_01=1, svUsed_01=0, health_01=1, diffCorr_01=0, smoothed_01=0, orbitSource_01=0, ephAvail_01=0, almAvail_01=0, anoAvail_01=0, aopAvail_01=0, sbasCorrUsed_01=0, rtcmCorrUsed_01=0, slasCorrUsed_01=0, spartnCorrUsed_01=0, prCorrUsed_01=0, crCorrUsed_01=0, doCorrUsed_01=0, gnssId_02=GPS, svId_02=14, cno_02=23, elev_02=50, azim_02=87, prRes_02=31, qualityInd_02=4, svUsed_02=1, health_02=1, diffCorr_02=0, smoothed_02=0, orbitSource_02=1, ephAvail_02=1, almAvail_02=1, anoAvail_02=0, aopAvail_02=1, sbasCorrUsed_02=0, rtcmCorrUsed_02=0, slasCorrUsed_02=0, spartnCorrUsed_02=0, prCorrUsed_02=0, crCorrUsed_02=0, doCorrUsed_02=0, gnssId_03=GPS, svId_03=15, cno_03=26, elev_03=-91, azim_03=0, prRes_03=0, qualityInd_03=7, svUsed_03=0, health_03=1, diffCorr_03=0, smoothed_03=0, orbitSource_03=0, ephAvail_03=0, almAvail_03=0, anoAvail_03=0, aopAvail_03=0, sbasCorrUsed_03=0, rtcmCorrUsed_03=0, slasCorrUsed_03=0, spartnCorrUsed_03=0, prCorrUsed_03=0, crCorrUsed_03=0, doCorrUsed_03=0, gnssId_04=GPS, svId_04=20, cno_04=15, elev_04=24, azim_04=313, prRes_04=0, qualityInd_04=4, svUsed_04=0, health_04=1, diffCorr_04=0, smoothed_04=0, orbitSource_04=2, ephAvail_04=0, almAvail_04=1, anoAvail_04=0, aopAvail_04=0, sbasCorrUsed_04=0, rtcmCorrUsed_04=0, slasCorrUsed_04=0, spartnCorrUsed_04=0, prCorrUsed_04=0, crCorrUsed_04=0, doCorrUsed_04=0, gnssId_05=GPS, svId_05=23, cno_05=17, elev_05=24, azim_05=315, prRes_05=0, qualityInd_05=4, svUsed_05=0, health_05=1, diffCorr_05=0, smoothed_05=0, orbitSource_05=2, ephAvail_05=0, almAvail_05=1, anoAvail_05=0, aopAvail_05=0, sbasCorrUsed_05=0, rtcmCorrUsed_05=0, slasCorrUsed_05=0, spartnCorrUsed_05=0, prCorrUsed_05=0, crCorrUsed_05=0, doCorrUsed_05=0, gnssId_06=GPS, svId_06=24, cno_06=36, elev_06=25, azim_06=247, prRes_06=-3, qualityInd_06=7, svUsed_06=1, health_06=1, diffCorr_06=0, smoothed_06=0, orbitSource_06=1, ephAvail_06=1, almAvail_06=1, anoAvail_06=0, aopAvail_06=1, sbasCorrUsed_06=0, rtcmCorrUsed_06=0, slasCorrUsed_06=0, spartnCorrUsed_06=0, prCorrUsed_06=0, crCorrUsed_06=0, doCorrUsed_06=0, gnssId_07=GPS, svId_07=30, cno_07=16, elev_07=-91, azim_07=0, prRes_07=0, qualityInd_07=4, svUsed_07=0, health_07=1, diffCorr_07=0, smoothed_07=0, orbitSource_07=0, ephAvail_07=0, almAvail_07=0, anoAvail_07=0, aopAvail_07=0, sbasCorrUsed_07=0, rtcmCorrUsed_07=0, slasCorrUsed_07=0, spartnCorrUsed_07=0, prCorrUsed_07=0, crCorrUsed_07=0, doCorrUsed_07=0, gnssId_08=SBAS, svId_08=127, cno_08=0, elev_08=10, azim_08=117, prRes_08=0, qualityInd_08=1, svUsed_08=0, health_08=0, diffCorr_08=0, smoothed_08=0, orbitSource_08=7, ephAvail_08=0, almAvail_08=0, anoAvail_08=0, aopAvail_08=0, sbasCorrUsed_08=0, rtcmCorrUsed_08=0, slasCorrUsed_08=0, spartnCorrUsed_08=0, prCorrUsed_08=0, crCorrUsed_08=0, doCorrUsed_08=0, gnssId_09=BeiDou, svId_09=15, cno_09=0, elev_09=-91, azim_09=0, prRes_09=0, qualityInd_09=1, svUsed_09=0, health_09=0, diffCorr_09=0, smoothed_09=0, orbitSource_09=0, ephAvail_09=0, almAvail_09=0, anoAvail_09=0, aopAvail_09=0, sbasCorrUsed_09=0, rtcmCorrUsed_09=0, slasCorrUsed_09=0, spartnCorrUsed_09=0, prCorrUsed_09=0, crCorrUsed_09=0, doCorrUsed_09=0, gnssId_10=GLONASS, svId_10=4, cno_10=0, elev_10=38, azim_10=144, prRes_10=0, qualityInd_10=0, svUsed_10=0, health_10=1, diffCorr_10=0, smoothed_10=0, orbitSource_10=2, ephAvail_10=0, almAvail_10=1, anoAvail_10=0, aopAvail_10=0, sbasCorrUsed_10=0, rtcmCorrUsed_10=0, slasCorrUsed_10=0, spartnCorrUsed_10=0, prCorrUsed_10=0, crCorrUsed_10=0, doCorrUsed_10=0, gnssId_11=GLONASS, svId_11=5, cno_11=22, elev_11=84, azim_11=272, prRes_11=53, qualityInd_11=4, svUsed_11=1, health_11=1, diffCorr_11=0, smoothed_11=0, orbitSource_11=1, ephAvail_11=1, almAvail_11=1, anoAvail_11=0, aopAvail_11=1, sbasCorrUsed_11=0, rtcmCorrUsed_11=0, slasCorrUsed_11=0, spartnCorrUsed_11=0, prCorrUsed_11=0, crCorrUsed_11=0, doCorrUsed_11=0, gnssId_12=GLONASS, svId_12=6, cno_12=0, elev_12=23, azim_12=318, prRes_12=0, qualityInd_12=0, svUsed_12=0, health_12=1, diffCorr_12=0, smoothed_12=0, orbitSource_12=2, ephAvail_12=0, almAvail_12=1, anoAvail_12=0, aopAvail_12=0, sbasCorrUsed_12=0, rtcmCorrUsed_12=0, slasCorrUsed_12=0, spartnCorrUsed_12=0, prCorrUsed_12=0, crCorrUsed_12=0, doCorrUsed_12=0, gnssId_13=GLONASS, svId_13=13, cno_13=0, elev_13=2, azim_13=39, prRes_13=0, qualityInd_13=0, svUsed_13=0, health_13=1, diffCorr_13=0, smoothed_13=0, orbitSource_13=2, ephAvail_13=0, almAvail_13=1, anoAvail_13=0, aopAvail_13=0, sbasCorrUsed_13=0, rtcmCorrUsed_13=0, slasCorrUsed_13=0, spartnCorrUsed_13=0, prCorrUsed_13=0, crCorrUsed_13=0, doCorrUsed_13=0, gnssId_14=GLONASS, svId_14=14, cno_14=23, elev_14=53, azim_14=47, prRes_14=0, qualityInd_14=4, svUsed_14=0, health_14=1, diffCorr_14=0, smoothed_14=0, orbitSource_14=2, ephAvail_14=0, almAvail_14=1, anoAvail_14=0, aopAvail_14=0, sbasCorrUsed_14=0, rtcmCorrUsed_14=0, slasCorrUsed_14=0, spartnCorrUsed_14=0, prCorrUsed_14=0, crCorrUsed_14=0, doCorrUsed_14=0, gnssId_15=GLONASS, svId_15=15, cno_15=36, elev_15=67, azim_15=201, prRes_15=9, qualityInd_15=7, svUsed_15=1, health_15=1, diffCorr_15=0, smoothed_15=0, orbitSource_15=1, ephAvail_15=1, almAvail_15=1, anoAvail_15=0, aopAvail_15=1, sbasCorrUsed_15=0, rtcmCorrUsed_15=0, slasCorrUsed_15=0, spartnCorrUsed_15=0, prCorrUsed_15=0, crCorrUsed_15=0, doCorrUsed_15=0, gnssId_16=GLONASS, svId_16=16, cno_16=0, elev_16=11, azim_16=216, prRes_16=0, qualityInd_16=0, svUsed_16=0, health_16=1, diffCorr_16=0, smoothed_16=0, orbitSource_16=2, ephAvail_16=0, almAvail_16=1, anoAvail_16=0, aopAvail_16=0, sbasCorrUsed_16=0, rtcmCorrUsed_16=0, slasCorrUsed_16=0, spartnCorrUsed_16=0, prCorrUsed_16=0, crCorrUsed_16=0, doCorrUsed_16=0, gnssId_17=GLONASS, svId_17=21, cno_17=0, elev_17=4, azim_17=301, prRes_17=0, qualityInd_17=0, svUsed_17=0, health_17=1, diffCorr_17=0, smoothed_17=0, orbitSource_17=2, ephAvail_17=0, almAvail_17=1, anoAvail_17=0, aopAvail_17=0, sbasCorrUsed_17=0, rtcmCorrUsed_17=0, slasCorrUsed_17=0, spartnCorrUsed_17=0, prCorrUsed_17=0, crCorrUsed_17=0, doCorrUsed_17=0, gnssId_18=GLONASS, svId_18=22, cno_18=0, elev_18=15, azim_18=346, prRes_18=0, qualityInd_18=0, svUsed_18=0, health_18=1, diffCorr_18=0, smoothed_18=0, orbitSource_18=2, ephAvail_18=0, almAvail_18=1, anoAvail_18=0, aopAvail_18=0, sbasCorrUsed_18=0, rtcmCorrUsed_18=0, slasCorrUsed_18=0, spartnCorrUsed_18=0, prCorrUsed_18=0, crCorrUsed_18=0, doCorrUsed_18=0, gnssId_19=GLONASS, svId_19=23, cno_19=0, elev_19=4, azim_19=47, prRes_19=0, qualityInd_19=0, svUsed_19=0, health_19=1, diffCorr_19=0, smoothed_19=0, orbitSource_19=2, ephAvail_19=0, almAvail_19=1, anoAvail_19=0, aopAvail_19=0, sbasCorrUsed_19=0, rtcmCorrUsed_19=0, slasCorrUsed_19=0, spartnCorrUsed_19=0, prCorrUsed_19=0, crCorrUsed_19=0, doCorrUsed_19=0)>",
            "<UBX(NAV-SIG, iTOW=09:08:09, version=0, numSigs=12, reserved0=0, gnssId_01=GPS, svId_01=3, sigId_01=0, freqId_01=0, prRes_01=0, cno_01=0, qualityInd_01=1, corrSource_01=0, ionoModel_01=0, health_01=1, prSmoothed_01=0, prUsed_01=0, crUsed_01=0, doUsed_01=0, prCorrUsed_01=0, crCorrUsed_01=0, doCorrUsed_01=0, reserved1_01=0, gnssId_02=GPS, svId_02=14, sigId_02=0, freqId_02=0, prRes_02=31, cno_02=23, qualityInd_02=4, corrSource_02=0, ionoModel_02=0, health_02=1, prSmoothed_02=0, prUsed_02=1, crUsed_02=0, doUsed_02=1, prCorrUsed_02=0, crCorrUsed_02=0, doCorrUsed_02=0, reserved1_02=0, gnssId_03=GPS, svId_03=15, sigId_03=0, freqId_03=0, prRes_03=0, cno_03=26, qualityInd_03=7, corrSource_03=0, ionoModel_03=0, health_03=1, prSmoothed_03=0, prUsed_03=0, crUsed_03=0, doUsed_03=0, prCorrUsed_03=0, crCorrUsed_03=0, doCorrUsed_03=0, reserved1_03=0, gnssId_04=GPS, svId_04=20, sigId_04=0, freqId_04=0, prRes_04=0, cno_04=15, qualityInd_04=4, corrSource_04=0, ionoModel_04=0, health_04=1, prSmoothed_04=0, prUsed_04=0, crUsed_04=0, doUsed_04=0, prCorrUsed_04=0, crCorrUsed_04=0, doCorrUsed_04=0, reserved1_04=0, gnssId_05=GPS, svId_05=23, sigId_05=0, freqId_05=0, prRes_05=0, cno_05=17, qualityInd_05=4, corrSource_05=0, ionoModel_05=0, health_05=1, prSmoothed_05=0, prUsed_05=0, crUsed_05=0, doUsed_05=0, prCorrUsed_05=0, crCorrUsed_05=0, doCorrUsed_05=0, reserved1_05=0, gnssId_06=GPS, svId_06=24, sigId_06=0, freqId_06=0, prRes_06=-3, cno_06=36, qualityInd_06=7, corrSource_06=0, ionoModel_06=0, health_06=1, prSmoothed_06=0, prUsed_06=1, crUsed_06=0, doUsed_06=1, prCorrUsed_06=0, crCorrUsed_06=0, doCorrUsed_06=0, reserved1_06=0, gnssId_07=GPS, svId_07=30, sigId_07=0, freqId_07=0, prRes_07=0, cno_07=16, qualityInd_07=4, corrSource_07=0, ionoModel_07=0, health_07=1, prSmoothed_07=0, prUsed_07=0, crUsed_07=0, doUsed_07=0, prCorrUsed_07=0, crCorrUsed_07=0, doCorrUsed_07=0, reserved1_07=0, gnssId_08=SBAS, svId_08=127, sigId_08=0, freqId_08=0, prRes_08=0, cno_08=0, qualityInd_08=1, corrSource_08=0, ionoModel_08=0, health_08=0, prSmoothed_08=0, prUsed_08=0, crUsed_08=0, doUsed_08=0, prCorrUsed_08=0, crCorrUsed_08=0, doCorrUsed_08=0, reserved1_08=0, gnssId_09=BeiDou, svId_09=15, sigId_09=0, freqId_09=0, prRes_09=0, cno_09=0, qualityInd_09=1, corrSource_09=0, ionoModel_09=0, health_09=0, prSmoothed_09=0, prUsed_09=0, crUsed_09=0, doUsed_09=0, prCorrUsed_09=0, crCorrUsed_09=0, doCorrUsed_09=0, reserved1_09=0, gnssId_10=GLONASS, svId_10=5, sigId_10=0, freqId_10=8, prRes_10=53, cno_10=22, qualityInd_10=4, corrSource_10=0, ionoModel_10=0, health_10=1, prSmoothed_10=0, prUsed_10=1, crUsed_10=0, doUsed_10=1, prCorrUsed_10=0, crCorrUsed_10=0, doCorrUsed_10=0, reserved1_10=0, gnssId_11=GLONASS, svId_11=14, sigId_11=0, freqId_11=0, prRes_11=0, cno_11=23, qualityInd_11=4, corrSource_11=0, ionoModel_11=0, health_11=1, prSmoothed_11=0, prUsed_11=0, crUsed_11=0, doUsed_11=0, prCorrUsed_11=0, crCorrUsed_11=0, doCorrUsed_11=0, reserved1_11=0, gnssId_12=GLONASS, svId_12=15, sigId_12=0, freqId_12=7, prRes_12=9, cno_12=36, qualityInd_12=7, corrSource_12=0, ionoModel_12=0, health_12=1, prSmoothed_12=0, prUsed_12=1, crUsed_12=0, doUsed_12=1, prCorrUsed_12=0, crCorrUsed_12=0, doCorrUsed_12=0, reserved1_12=0)>",
            "<UBX(NAV-STATUS, iTOW=09:08:09, gpsFix=3, gpsFixOk=1, diffSoln=0, wknSet=1, towSet=1, diffCorr=0, carrSolnValid=0, mapMatching=0, psmState=0, spoofDetState=1, carrSoln=0, ttff=179368, msss=366244)>",
            "<UBX(NAV-POSECEF, iTOW=09:08:09, ecefX=380363892, ecefY=-14879221, ecefZ=510062895, pAcc=6570)>",
            "<UBX(NAV-POSLLH, iTOW=09:08:09, lon=-22401762, lat=534506799, height=72728, hMSL=24245, hAcc=55374, vAcc=35349)>",
            "<UBX(NAV-DOP, iTOW=09:08:09, gDOP=570, pDOP=520, tDOP=233, vDOP=276, hDOP=441, nDOP=410, eDOP=161)>",
            "<UBX(NAV-VELECEF, iTOW=09:08:09, ecefVX=-25, ecefVY=-4, ecefVZ=27, sAcc=451)>",
            "<UBX(NAV-VELNED, iTOW=09:08:09, velN=36, velE=-5, velD=-7, speed=37, gSpeed=37, heading=0, sAcc=451, cAcc=13597116)>",
            "<UBX(NAV-TIMEGPS, iTOW=09:08:09, fTOW=332986, week=2146, leapS=18, towValid=1, weekValid=1, leapSValid=1, tAcc=71)>",
            "<UBX(NAV-TIMEGLO, iTOW=09:08:09, TOD=43687, fTOD=332964, Nt=419, N4=7, todValid=1, dateValid=1, tAcc=101)>",
            "<UBX(NAV-TIMEBDS, iTOW=09:08:09, SOW=119291, fSOW=332986, week=790, leapS=4, sowValid=1, weekValid=1, leapSValid=1, tAcc=3406)>",
            "<UBX(NAV-TIMEGAL, iTOW=09:08:09, galTow=119305, fGalTow=332986, galWno=1122, leapS=18, galTowValid=1, galWnoValid=1, leapSValid=1, tAcc=3406)>",
            "<UBX(NAV-TIMEUTC, iTOW=09:08:09, tAcc=1071, nano=332985, year=2021, month=2, day=22, hour=9, min=8, sec=7, validTOW=1, validWKN=1, validUTC=1, utcStandard=15)>",
            "<UBX(NAV-TIMELS, iTOW=09:08:09, version=0, reserved1=0, srcOfCurrLs=255, currLs=18, srcOfLsChange=6, lsChange=0, timeToLsEvent=-32887, dateOfLsGpsWn=2146, dateOfLsGpsDn=1, reserved2=0, validCurrLs=1, validTimeToLsEvent=1)>",
            "<UBX(NAV-TIMEQZSS, iTOW=09:08:09, qzssTow=119305, fQzssTow=332986, qzssWno=2146, leapS=18, qzssTowValid=1, qzssWnoValid=1, leapSValid=1, tAcc=3406)>",
            "<UBX(NAV-CLOCK, iTOW=09:08:09, clkB=667014, clkD=-71, tAcc=71, fAcc=5239)>",
            "<UBX(NAV-SBAS, iTOW=09:08:09, geo=0, mode=0, sys=0, Ranging=0, Corrections=0, Integrity=0, Testmode=0, Bad=0, numCh=0, integrityUsed=0, reserved0=0)>",
            "<UBX(NAV-SLAS, iTOW=09:08:09, version=0, reserved1=0, gmsLon=0, gmsLat=0, gmsCode=0, qzssSvId=0, gmsAvailable=0, qzssSvAvailable=0, testMode=0, cnt=0)>",
            "<UBX(NAV-AOPSTATUS, iTOW=09:08:09, config=1, status=0, reserved0=0, reserved1=10, avail=0, reserved2=0, reserved3=0)>",
            "<UBX(NAV-ODO, version=0, reserved0=466035, iTOW=09:08:09, distance=0, totalDistance=0, distanceStd=0)>",
            "<UBX(NAV-COV, iTOW=09:08:09, version=0, posCovValid=1, velCovValid=1, reserved0=1172170281114452235776, posCovNN=2530.31201171875, posCovNE=-856.8651123046875, posCovND=-1116.0887451171875, posCovEE=535.9963989257812, posCovED=742.3728637695312, posCovDD=1249.5338134765625, velCovNN=17.608617782592773, velCovNE=-4.361900329589844, velCovND=-5.844054222106934, velCovEE=2.3484761714935303, velCovED=2.9350130558013916, velCovDD=4.592257499694824)>",
            "<UBX(NAV-EELL, iTOW=09:08:09, version=0, reserved1=0, errEllipseOrient=15966, errEllipseMajor=132667, errEllipseMinor=36740)>",
            "<UBX(NAV-GEOFENCE, iTOW=09:08:09, version=0, status=0, numFences=0, combState=0)>",
        )

        i = 0
        raw = 0
        ubxreader = UBXReader(self.streamMIX2, False)
        while raw is not None:
            (raw, parsed) = ubxreader.read()
            if raw is not None:
                self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                i += 1

    def testMIX2VAL(self):  # test mixed UBX/NMEA stream with validate set to True
        EXPECTED_ERROR = "Unknown data header b'$G'. Looks like NMEA data. Set ubxonly flag to 'False' to ignore."
        ubxreader = UBXReader(self.streamMIX2, True)
        with self.assertRaises(UBXStreamError) as context:
            (_, _) = ubxreader.read()
        self.assertTrue(EXPECTED_ERROR in str(context.exception))

    def testINF(self):
        EXPECTED_RESULTS = (
            "<UBX(INF-NOTICE, message=u-blox AG - www.u-blox.com)>",
            "<UBX(INF-NOTICE, message=HW UBX-M8030 00080000)>",
            "<UBX(INF-NOTICE, message=ROM CORE 3.01 (107888))>",
            "<UBX(INF-NOTICE, message=FWVER=SPG 3.01)>",
            "<UBX(INF-NOTICE, message=PROTVER=18.00)>",
            "<UBX(INF-NOTICE, message=GPS;GLO;GAL;BDS)>",
            "<UBX(INF-NOTICE, message=SBAS;IMES;QZSS)>",
            "<UBX(INF-NOTICE, message=GNSS OTP=GPS;GLO)>",
            "<UBX(INF-NOTICE, message=LLC=FFFFFFFF-FFFFFFFF-FFFFFFFF-FFFFFFFF-FFFFFFFD)>",
            "<UBX(INF-NOTICE, message=ANTSUPERV=AC SD PDoS SR)>",
            "<UBX(INF-NOTICE, message=ANTSTATUS=OK)>",
            "<UBX(INF-NOTICE, message=PF=3FF)>",
        )

        i = 0
        raw = 0
        ubxreader = UBXReader(self.streamINF, ubxonly=False)
        while raw is not None:
            (raw, parsed) = ubxreader.read()
            if raw is not None:
                self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                i += 1

    def testMON(self):
        EXPECTED_RESULTS = (
            "<UBX(MON-MSGPP, msg1_01=0, msg1_02=0, msg1_03=0, msg1_04=0, msg1_05=0, msg1_06=0, msg1_07=0, msg1_08=0, msg2_01=0, msg2_02=0, msg2_03=0, msg2_04=0, msg2_05=0, msg2_06=0, msg2_07=0, msg2_08=0, msg3_01=0, msg3_02=0, msg3_03=0, msg3_04=0, msg3_05=0, msg3_06=0, msg3_07=0, msg3_08=0, msg4_01=69, msg4_02=0, msg4_03=0, msg4_04=0, msg4_05=0, msg4_06=0, msg4_07=0, msg4_08=0, msg5_01=0, msg5_02=0, msg5_03=0, msg5_04=0, msg5_05=0, msg5_06=0, msg5_07=0, msg5_08=0, msg6_01=0, msg6_02=0, msg6_03=0, msg6_04=0, msg6_05=0, msg6_06=0, msg6_07=0, msg6_08=0, skipped_01=0, skipped_02=0, skipped_03=0, skipped_04=0, skipped_05=0, skipped_06=0)>",
            "<UBX(MON-TXBUF, pending_01=0, pending_02=0, pending_03=0, pending_04=0, pending_05=0, pending_06=0, usage_01=0, usage_02=2, usage_03=0, usage_04=0, usage_05=0, usage_06=0, peakUsage_01=0, peakUsage_02=12, peakUsage_03=0, peakUsage_04=25, peakUsage_05=0, peakUsage_06=0, tUsage=2, tPeakUsage=25, txErrorLimit=0, txErrorMem=0, txErrorAlloc=0, reserved1=0)>",
            "<UBX(MON-RXBUF, pending_01=0, pending_02=0, pending_03=0, pending_04=0, pending_05=0, pending_06=0, usage_01=0, usage_02=0, usage_03=0, usage_04=0, usage_05=0, usage_06=0, peakUsage_01=0, peakUsage_02=0, peakUsage_03=0, peakUsage_04=2, peakUsage_05=0, peakUsage_06=0)>",
            "<UBX(MON-IO, rxBytes=0, txBytes=0, parityErrs=0, framingErrs=0, overrunErrs=0, breakCond=0, rxBusy=0, txBusy=0, reserved1=0)>",
            "<UBX(MON-HW, pinSel=b'\\x00\\xf4\\x01\\x00', pinBank=b'\\x00\\x00\\x00\\x00', pinDir=b'\\x00\\x00\\x01\\x00', pinVal=b'\\xef\\xf7\\x00\\x00', noisePerMS=87, agcCnt=3042, aStatus=2, aPower=1, rtcCalib=1, safeBoot=0, jammingState=0, xtalAbsent=0, reserved1=132, usedMask=b'\\xff\\xeb\\x01\\x00', VP_01=b'\\n', VP_02=b'\\x0b', VP_03=b'\\x0c', VP_04=b'\\r', VP_05=b'\\x0e', VP_06=b'\\x0f', VP_07=b'\\x01', VP_08=b'\\x00', VP_09=b'\\x02', VP_10=b'\\x03', VP_11=b'\\xff', VP_12=b'\\x10', VP_13=b'\\xff', VP_14=b'\\x12', VP_15=b'\\x13', VP_16=b'6', VP_17=b'5', VP_18=b'\\x05', VP_19=b'\\xef', VP_20=b'^', VP_21=b'\\x00', VP_22=b'\\x00', VP_23=b'\\x00', VP_24=b'\\x00', VP_25=b'\\x80', jamInd=247, reserved3=0, pinIrq=b'\\x00\\x00\\x00\\x00', pullH=b'', pullL=b'')>",
            "<UBX(MON-HW2, ofsI=4, magI=110, ofsQ=5, magQ=112, cfgSource=111, reserved0=1800, lowLevCfg=4294967295, reserved11=4294967295, reserved12=4294967295, postStatus=0, reserved2=0)>",
        )

        i = 0
        raw = 0
        ubxreader = UBXReader(self.streamMON)
        while raw is not None:
            (raw, parsed) = ubxreader.read()
            if raw is not None:
                self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                i += 1

    def testMON2(self):  # test with parsebitfield set to False
        EXPECTED_RESULTS = (
            "<UBX(MON-MSGPP, msg1_01=0, msg1_02=0, msg1_03=0, msg1_04=0, msg1_05=0, msg1_06=0, msg1_07=0, msg1_08=0, msg2_01=0, msg2_02=0, msg2_03=0, msg2_04=0, msg2_05=0, msg2_06=0, msg2_07=0, msg2_08=0, msg3_01=0, msg3_02=0, msg3_03=0, msg3_04=0, msg3_05=0, msg3_06=0, msg3_07=0, msg3_08=0, msg4_01=69, msg4_02=0, msg4_03=0, msg4_04=0, msg4_05=0, msg4_06=0, msg4_07=0, msg4_08=0, msg5_01=0, msg5_02=0, msg5_03=0, msg5_04=0, msg5_05=0, msg5_06=0, msg5_07=0, msg5_08=0, msg6_01=0, msg6_02=0, msg6_03=0, msg6_04=0, msg6_05=0, msg6_06=0, msg6_07=0, msg6_08=0, skipped_01=0, skipped_02=0, skipped_03=0, skipped_04=0, skipped_05=0, skipped_06=0)>",
            "<UBX(MON-TXBUF, pending_01=0, pending_02=0, pending_03=0, pending_04=0, pending_05=0, pending_06=0, usage_01=0, usage_02=2, usage_03=0, usage_04=0, usage_05=0, usage_06=0, peakUsage_01=0, peakUsage_02=12, peakUsage_03=0, peakUsage_04=25, peakUsage_05=0, peakUsage_06=0, tUsage=2, tPeakUsage=25, errors=b'\\x00', reserved1=0)>",
            "<UBX(MON-RXBUF, pending_01=0, pending_02=0, pending_03=0, pending_04=0, pending_05=0, pending_06=0, usage_01=0, usage_02=0, usage_03=0, usage_04=0, usage_05=0, usage_06=0, peakUsage_01=0, peakUsage_02=0, peakUsage_03=0, peakUsage_04=2, peakUsage_05=0, peakUsage_06=0)>",
            "<UBX(MON-IO, rxBytes=0, txBytes=0, parityErrs=0, framingErrs=0, overrunErrs=0, breakCond=0, rxBusy=0, txBusy=0, reserved1=0)>",
            "<UBX(MON-HW, pinSel=b'\\x00\\xf4\\x01\\x00', pinBank=b'\\x00\\x00\\x00\\x00', pinDir=b'\\x00\\x00\\x01\\x00', pinVal=b'\\xef\\xf7\\x00\\x00', noisePerMS=87, agcCnt=3042, aStatus=2, aPower=1, flags=b'\\x01', reserved1=132, usedMask=b'\\xff\\xeb\\x01\\x00', VP_01=b'\\n', VP_02=b'\\x0b', VP_03=b'\\x0c', VP_04=b'\\r', VP_05=b'\\x0e', VP_06=b'\\x0f', VP_07=b'\\x01', VP_08=b'\\x00', VP_09=b'\\x02', VP_10=b'\\x03', VP_11=b'\\xff', VP_12=b'\\x10', VP_13=b'\\xff', VP_14=b'\\x12', VP_15=b'\\x13', VP_16=b'6', VP_17=b'5', VP_18=b'\\x05', VP_19=b'\\xef', VP_20=b'^', VP_21=b'\\x00', VP_22=b'\\x00', VP_23=b'\\x00', VP_24=b'\\x00', VP_25=b'\\x80', jamInd=247, reserved3=0, pinIrq=b'\\x00\\x00\\x00\\x00', pullH=b'', pullL=b'')>",
            "<UBX(MON-HW2, ofsI=4, magI=110, ofsQ=5, magQ=112, cfgSource=111, reserved0=1800, lowLevCfg=4294967295, reserved11=4294967295, reserved12=4294967295, postStatus=0, reserved2=0)>",
        )

        i = 0
        raw = 0
        ubxreader = UBXReader(self.streamMON, parsebitfield=False)
        while raw is not None:
            (raw, parsed) = ubxreader.read()
            if raw is not None:
                self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                i += 1

    # TODO uncomment test when RXM-SFRBX decoder ready
    # def testRXM(self):
    #     EXPECTED_RESULTS = (
    #         "<UBX(RXM-MEASX, version=1, reserved0=0, gpsTOW=231234000, gloTOW=242016000, bdsTOW=231220000, reserved1=231234000, qzssTOW=1000, gpsTOWacc=0, gloTOWacc=0, bdsTOWacc=0, reserved2=0, qzssTOWacc=0, numSv=9, towSet=2, reserved3=0, gnssId_01=QZSS, svId_01=1, cNo_01=12, mpathIndic_01=1, dopplerMS_01=11538, dopplerHz_01=12126, wholeChips_01=809, fracChips_01=24, codePhase_01=1658502, intCodePhase_01=0, pseuRangeRMSErr_01=52, reserved4_01=0, gnssId_02=GPS, svId_02=18, cNo_02=17, mpathIndic_02=1, dopplerMS_02=2646, dopplerHz_02=2781, wholeChips_02=858, fracChips_02=265, codePhase_02=1759434, intCodePhase_02=0, pseuRangeRMSErr_02=46, reserved4_02=0, gnssId_03=GPS, svId_03=28, cNo_03=18, mpathIndic_03=1, dopplerMS_03=10576, dopplerHz_03=11115, wholeChips_03=536, fracChips_03=533, codePhase_03=1099868, intCodePhase_03=0, pseuRangeRMSErr_03=46, reserved4_03=0, gnssId_04=GLONASS, svId_04=8, cNo_04=17, mpathIndic_04=1, dopplerMS_04=11949, dopplerHz_04=12797, wholeChips_04=55, fracChips_04=693, codePhase_04=228499, intCodePhase_04=0, pseuRangeRMSErr_04=46, reserved4_04=0, gnssId_05=GLONASS, svId_05=9, cNo_05=25, mpathIndic_05=1, dopplerMS_05=4320, dopplerHz_05=4614, wholeChips_05=279, fracChips_05=102, codePhase_05=1145429, intCodePhase_05=0, pseuRangeRMSErr_05=27, reserved4_05=0, gnssId_06=GLONASS, svId_06=7, cNo_06=24, mpathIndic_06=1, dopplerMS_06=-3672, dopplerHz_06=-3931, wholeChips_06=100, fracChips_06=156, codePhase_06=411030, intCodePhase_06=0, pseuRangeRMSErr_06=46, reserved4_06=0, gnssId_07=GPS, svId_07=7, cNo_07=13, mpathIndic_07=1, dopplerMS_07=-14783, dopplerHz_07=-15537, wholeChips_07=947, fracChips_07=989, codePhase_07=1943334, intCodePhase_07=0, pseuRangeRMSErr_07=52, reserved4_07=0, gnssId_08=GPS, svId_08=13, cNo_08=28, mpathIndic_08=1, dopplerMS_08=5649, dopplerHz_08=5937, wholeChips_08=239, fracChips_08=545, codePhase_08=491043, intCodePhase_08=0, pseuRangeRMSErr_08=15, reserved4_08=0, gnssId_09=GPS, svId_09=5, cNo_09=32, mpathIndic_09=1, dopplerMS_09=-9606, dopplerHz_09=-10096, wholeChips_09=220, fracChips_09=411, codePhase_09=451825, intCodePhase_09=0, pseuRangeRMSErr_09=18, reserved4_09=0)>",
    #         "<UBX(RXM-SVSI, iTOW=16:13:38, week=2128, numVis=24, numSV=190, svid=1, svFlag=b'_', azim=82, elev=-49, age=b'\\xf2')>",
    #         "<UBX(RXM-IMES, numTx=0, version=1, reserved1=0)>",
    #         "<UBX(RXM-SFRBX, gnssId=GPS, svId=5, reserved0=0, freqId=0, numWords=10, chn=0, version=2, reserved1=0, dwrd_01=583028782, dwrd_02=2463198336, dwrd_03=394902765, dwrd_04=2566867280, dwrd_05=1062207503, dwrd_06=675481840, dwrd_07=616371498, dwrd_08=2740700967, dwrd_09=768066377, dwrd_10=3045061856)>",
    #     )

    #     i = 0
    #     raw = 0
    #     ubxreader = UBXReader(self.streamRXM)
    #     while raw is not None:
    #         (raw, parsed) = ubxreader.read()
    #         if raw is not None:
    #             self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
    #             i += 1

    def testHNR(self):  # test 20Hz high rate navigation messages
        EXPECTED_RESULTS = (
            "<UBX(HNR-PVT, iTOW=09:15:01.400000, year=2021, month=4, day=16, hour=9, min=14, second=59, validDate=1, validTime=1, fullyResolved=1, nano=400000109, gpsFix=3, GPSfixOK=1, DiffSoln=0, WKNSET=1, TOWSET=1, headVehValid=1, reserved1=3999, lon=45161898, lat=518927505, height=68308, hMSL=22326, gSpeed=477, speed=502, headMot=26585090, headVeh=26585090, hAcc=36541, vAcc=49102, sAcc=1557, headAcc=3887061, reserved2=775501108)>",
            "<UBX(HNR-PVT, iTOW=09:15:01.450000, year=2021, month=4, day=16, hour=9, min=14, second=59, validDate=1, validTime=1, fullyResolved=1, nano=450000110, gpsFix=3, GPSfixOK=1, DiffSoln=0, WKNSET=1, TOWSET=1, headVehValid=1, reserved1=4499, lon=45161895, lat=518927505, height=68316, hMSL=22334, gSpeed=477, speed=502, headMot=26585090, headVeh=26585090, hAcc=36541, vAcc=49102, sAcc=1557, headAcc=3887061, reserved2=775501108)>",
            "<UBX(HNR-PVT, iTOW=09:15:01.500000, year=2021, month=4, day=16, hour=9, min=14, second=59, validDate=1, validTime=1, fullyResolved=1, nano=500000111, gpsFix=3, GPSfixOK=1, DiffSoln=0, WKNSET=1, TOWSET=1, headVehValid=1, reserved1=4999, lon=45161891, lat=518927505, height=68324, hMSL=22342, gSpeed=477, speed=502, headMot=26585090, headVeh=26585090, hAcc=36541, vAcc=49102, sAcc=1557, headAcc=3887061, reserved2=775501108)>",
            "<UBX(HNR-PVT, iTOW=09:15:01.550000, year=2021, month=4, day=16, hour=9, min=14, second=59, validDate=1, validTime=1, fullyResolved=1, nano=550000112, gpsFix=3, GPSfixOK=1, DiffSoln=0, WKNSET=1, TOWSET=1, headVehValid=1, reserved1=5499, lon=45161888, lat=518927505, height=68332, hMSL=22350, gSpeed=477, speed=502, headMot=26585090, headVeh=26585090, hAcc=36541, vAcc=49102, sAcc=1557, headAcc=3887061, reserved2=775501108)>",
            "<UBX(HNR-PVT, iTOW=09:15:01.600000, year=2021, month=4, day=16, hour=9, min=14, second=59, validDate=1, validTime=1, fullyResolved=1, nano=600000112, gpsFix=3, GPSfixOK=1, DiffSoln=0, WKNSET=1, TOWSET=1, headVehValid=1, reserved1=5999, lon=45161884, lat=518927505, height=68340, hMSL=22358, gSpeed=477, speed=502, headMot=26585090, headVeh=26585090, hAcc=36541, vAcc=49102, sAcc=1557, headAcc=3887061, reserved2=775501108)>",
            "<UBX(HNR-PVT, iTOW=09:15:01.650000, year=2021, month=4, day=16, hour=9, min=14, second=59, validDate=1, validTime=1, fullyResolved=1, nano=650000113, gpsFix=3, GPSfixOK=1, DiffSoln=0, WKNSET=1, TOWSET=1, headVehValid=1, reserved1=6499, lon=45161881, lat=518927505, height=68348, hMSL=22366, gSpeed=477, speed=502, headMot=26585090, headVeh=26585090, hAcc=36541, vAcc=49102, sAcc=1557, headAcc=3887061, reserved2=775501108)>",
            "<UBX(HNR-PVT, iTOW=09:15:01.700000, year=2021, month=4, day=16, hour=9, min=14, second=59, validDate=1, validTime=1, fullyResolved=1, nano=700000114, gpsFix=3, GPSfixOK=1, DiffSoln=0, WKNSET=1, TOWSET=1, headVehValid=1, reserved1=6999, lon=45161877, lat=518927505, height=68356, hMSL=22374, gSpeed=477, speed=502, headMot=26585090, headVeh=26585090, hAcc=36541, vAcc=49102, sAcc=1557, headAcc=3887061, reserved2=775501108)>",
            "<UBX(HNR-PVT, iTOW=09:15:01.750000, year=2021, month=4, day=16, hour=9, min=14, second=59, validDate=1, validTime=1, fullyResolved=1, nano=750000115, gpsFix=3, GPSfixOK=1, DiffSoln=0, WKNSET=1, TOWSET=1, headVehValid=1, reserved1=7499, lon=45161874, lat=518927505, height=68364, hMSL=22382, gSpeed=477, speed=502, headMot=26585090, headVeh=26585090, hAcc=36541, vAcc=49102, sAcc=1557, headAcc=3887061, reserved2=775501108)>",
            "<UBX(HNR-PVT, iTOW=09:15:01.800000, year=2021, month=4, day=16, hour=9, min=14, second=59, validDate=1, validTime=1, fullyResolved=1, nano=800000115, gpsFix=3, GPSfixOK=1, DiffSoln=0, WKNSET=1, TOWSET=1, headVehValid=1, reserved1=7999, lon=45161870, lat=518927506, height=68372, hMSL=22390, gSpeed=477, speed=502, headMot=26585090, headVeh=26585090, hAcc=36541, vAcc=49102, sAcc=1557, headAcc=3887061, reserved2=775501108)>",
            "<UBX(HNR-PVT, iTOW=09:15:01.850000, year=2021, month=4, day=16, hour=9, min=14, second=59, validDate=1, validTime=1, fullyResolved=1, nano=850000116, gpsFix=3, GPSfixOK=1, DiffSoln=0, WKNSET=1, TOWSET=1, headVehValid=1, reserved1=8499, lon=45161867, lat=518927506, height=68380, hMSL=22398, gSpeed=477, speed=502, headMot=26585090, headVeh=26585090, hAcc=36541, vAcc=49102, sAcc=1557, headAcc=3887061, reserved2=775501108)>",
            "<UBX(HNR-PVT, iTOW=09:15:01.900000, year=2021, month=4, day=16, hour=9, min=14, second=59, validDate=1, validTime=1, fullyResolved=1, nano=900000117, gpsFix=3, GPSfixOK=1, DiffSoln=0, WKNSET=1, TOWSET=1, headVehValid=1, reserved1=8999, lon=45161863, lat=518927506, height=68388, hMSL=22406, gSpeed=477, speed=502, headMot=26585090, headVeh=26585090, hAcc=36541, vAcc=49102, sAcc=1557, headAcc=3887061, reserved2=775501108)>",
            "<UBX(HNR-PVT, iTOW=09:15:01.950000, year=2021, month=4, day=16, hour=9, min=14, second=59, validDate=1, validTime=1, fullyResolved=1, nano=950000118, gpsFix=3, GPSfixOK=1, DiffSoln=0, WKNSET=1, TOWSET=1, headVehValid=1, reserved1=9499, lon=45161860, lat=518927506, height=68396, hMSL=22414, gSpeed=477, speed=502, headMot=26585090, headVeh=26585090, hAcc=36541, vAcc=49102, sAcc=1557, headAcc=3887061, reserved2=775501108)>",
            "<UBX(HNR-PVT, iTOW=09:15:02, year=2021, month=4, day=16, hour=9, min=15, second=0, validDate=1, validTime=1, fullyResolved=1, nano=118, gpsFix=3, GPSfixOK=1, DiffSoln=0, WKNSET=1, TOWSET=1, headVehValid=1, reserved1=9999, lon=45161857, lat=518927506, height=68404, hMSL=22422, gSpeed=477, speed=502, headMot=26585090, headVeh=26585090, hAcc=36541, vAcc=49102, sAcc=1557, headAcc=3887061, reserved2=775501108)>",
        )

        i = 0
        raw = 0
        ubxreader = UBXReader(self.streamHNR, ubxonly=False)
        while raw is not None:
            (raw, parsed) = ubxreader.read()
            if raw is not None:
                self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                i += 1

    # TODO uncomment test when RXM-SFRBX decoder ready
    # def testIterator(self):  # test iterator function with UBX data stream
    #     EXPECTED_RESULTS = (
    #         "<UBX(RXM-MEASX, version=1, reserved0=0, gpsTOW=231234000, gloTOW=242016000, bdsTOW=231220000, reserved1=231234000, qzssTOW=1000, gpsTOWacc=0, gloTOWacc=0, bdsTOWacc=0, reserved2=0, qzssTOWacc=0, numSv=9, towSet=2, reserved3=0, gnssId_01=QZSS, svId_01=1, cNo_01=12, mpathIndic_01=1, dopplerMS_01=11538, dopplerHz_01=12126, wholeChips_01=809, fracChips_01=24, codePhase_01=1658502, intCodePhase_01=0, pseuRangeRMSErr_01=52, reserved4_01=0, gnssId_02=GPS, svId_02=18, cNo_02=17, mpathIndic_02=1, dopplerMS_02=2646, dopplerHz_02=2781, wholeChips_02=858, fracChips_02=265, codePhase_02=1759434, intCodePhase_02=0, pseuRangeRMSErr_02=46, reserved4_02=0, gnssId_03=GPS, svId_03=28, cNo_03=18, mpathIndic_03=1, dopplerMS_03=10576, dopplerHz_03=11115, wholeChips_03=536, fracChips_03=533, codePhase_03=1099868, intCodePhase_03=0, pseuRangeRMSErr_03=46, reserved4_03=0, gnssId_04=GLONASS, svId_04=8, cNo_04=17, mpathIndic_04=1, dopplerMS_04=11949, dopplerHz_04=12797, wholeChips_04=55, fracChips_04=693, codePhase_04=228499, intCodePhase_04=0, pseuRangeRMSErr_04=46, reserved4_04=0, gnssId_05=GLONASS, svId_05=9, cNo_05=25, mpathIndic_05=1, dopplerMS_05=4320, dopplerHz_05=4614, wholeChips_05=279, fracChips_05=102, codePhase_05=1145429, intCodePhase_05=0, pseuRangeRMSErr_05=27, reserved4_05=0, gnssId_06=GLONASS, svId_06=7, cNo_06=24, mpathIndic_06=1, dopplerMS_06=-3672, dopplerHz_06=-3931, wholeChips_06=100, fracChips_06=156, codePhase_06=411030, intCodePhase_06=0, pseuRangeRMSErr_06=46, reserved4_06=0, gnssId_07=GPS, svId_07=7, cNo_07=13, mpathIndic_07=1, dopplerMS_07=-14783, dopplerHz_07=-15537, wholeChips_07=947, fracChips_07=989, codePhase_07=1943334, intCodePhase_07=0, pseuRangeRMSErr_07=52, reserved4_07=0, gnssId_08=GPS, svId_08=13, cNo_08=28, mpathIndic_08=1, dopplerMS_08=5649, dopplerHz_08=5937, wholeChips_08=239, fracChips_08=545, codePhase_08=491043, intCodePhase_08=0, pseuRangeRMSErr_08=15, reserved4_08=0, gnssId_09=GPS, svId_09=5, cNo_09=32, mpathIndic_09=1, dopplerMS_09=-9606, dopplerHz_09=-10096, wholeChips_09=220, fracChips_09=411, codePhase_09=451825, intCodePhase_09=0, pseuRangeRMSErr_09=18, reserved4_09=0)>",
    #         "<UBX(RXM-SVSI, iTOW=16:13:38, week=2128, numVis=24, numSV=190, svid=1, svFlag=b'_', azim=82, elev=-49, age=b'\\xf2')>",
    #         "<UBX(RXM-IMES, numTx=0, version=1, reserved1=0)>",
    #         "<UBX(RXM-SFRBX, gnssId=GPS, svId=5, reserved0=0, freqId=0, numWords=10, chn=0, version=2, reserved1=0, dwrd_01=583028782, dwrd_02=2463198336, dwrd_03=394902765, dwrd_04=2566867280, dwrd_05=1062207503, dwrd_06=675481840, dwrd_07=616371498, dwrd_08=2740700967, dwrd_09=768066377, dwrd_10=3045061856)>",
    #     )

    #     i = 0
    #     ubxreader = UBXReader(self.streamRXM, True)
    #     for (_, parsed) in ubxreader:
    #         self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
    #         i += 1

    def testIterator2(self):  # test iterator function with mixed data stream
        EXPECTED_ERROR = "Unknown data header b'$G'. Looks like NMEA data. Set ubxonly flag to 'False' to ignore."
        ubxreader = UBXReader(self.streamMIX, ubxonly=True)
        with self.assertRaises(UBXStreamError) as context:
            i = 0
            #             (raw, parsed) = ubxreader.read()
            for (_, _) in ubxreader:
                i += 1
        self.assertTrue(EXPECTED_ERROR in str(context.exception))

    def testIterator3(self):  # test iterator function with mixed data stream
        EXPECTED_RESULTS = (
            "<UBX(NAV-SOL, iTOW=11:33:17, fTOW=52790, week=2128, gpsFix=3, gpsfixOK=1, diffSoln=0, wknSet=1, towSet=1, ecefX=380364134, ecefY=-14880030, ecefZ=510063062, pAcc=1026, ecefVX=-3, ecefVY=0, ecefVZ=1, sAcc=72, pDOP=135, reserved1=2, numSV=15, reserved2=215776)>",
            "<UBX(NAV-PVT, iTOW=11:33:17, year=2020, month=10, day=23, hour=11, min=33, second=15, validDate=1, validTime=1, fullyResolved=1, validMag=0, tAcc=17, nano=52792, fixType=3, gnssFixOk=1, difSoln=0, psmState=0, headVehValid=0, carrSoln=0, confirmedAvai=0, confirmedDate=0, confirmedTime=0, numSV=15, lon=-22402964, lat=534506691, height=75699, hMSL=27215, hAcc=6298, vAcc=8101, velN=27, velE=-4, velD=11, gSpeed=27, headMot=770506, sAcc=715, headAcc=3905453, pDOP=135, reserved1=151580049408, headVeh=0, magDec=0, magAcc=0)>",
            "<UBX(NAV-SVINFO, iTOW=11:33:17, numCh=25, chipGen=4, reserved2=0, chn_01=13, svid_01=1, svUsed_01=0, diffCorr_01=0, orbitAvail_01=1, orbitEph_01=1, unhealthy_01=0, orbitAlm_01=0, orbitAop_01=0, smoothed_01=0, qualityInd_01=1, cno_01=0, elev_01=4, azim_01=142, prRes_01=0, chn_02=19, svid_02=2, svUsed_02=0, diffCorr_02=0, orbitAvail_02=1, orbitEph_02=0, unhealthy_02=0, orbitAlm_02=0, orbitAop_02=0, smoothed_02=0, qualityInd_02=1, cno_02=0, elev_02=19, azim_02=311, prRes_02=0, chn_03=3, svid_03=3, svUsed_03=1, diffCorr_03=0, orbitAvail_03=1, orbitEph_03=1, unhealthy_03=0, orbitAlm_03=0, orbitAop_03=0, smoothed_03=0, qualityInd_03=4, cno_03=24, elev_03=41, azim_03=89, prRes_03=469, chn_04=0, svid_04=4, svUsed_04=1, diffCorr_04=0, orbitAvail_04=1, orbitEph_04=1, unhealthy_04=0, orbitAlm_04=0, orbitAop_04=0, smoothed_04=0, qualityInd_04=7, cno_04=26, elev_04=70, azim_04=98, prRes_04=94, chn_05=1, svid_05=6, svUsed_05=1, diffCorr_05=0, orbitAvail_05=1, orbitEph_05=1, unhealthy_05=0, orbitAlm_05=0, orbitAop_05=0, smoothed_05=0, qualityInd_05=7, cno_05=29, elev_05=61, azim_05=287, prRes_05=-1023, chn_06=255, svid_06=7, svUsed_06=0, diffCorr_06=0, orbitAvail_06=1, orbitEph_06=0, unhealthy_06=0, orbitAlm_06=0, orbitAop_06=0, smoothed_06=0, qualityInd_06=0, cno_06=0, elev_06=0, azim_06=168, prRes_06=0, chn_07=2, svid_07=9, svUsed_07=1, diffCorr_07=0, orbitAvail_07=1, orbitEph_07=1, unhealthy_07=0, orbitAlm_07=0, orbitAop_07=0, smoothed_07=0, qualityInd_07=7, cno_07=32, elev_07=56, azim_07=200, prRes_07=-18, chn_08=23, svid_08=12, svUsed_08=0, diffCorr_08=0, orbitAvail_08=1, orbitEph_08=0, unhealthy_08=0, orbitAlm_08=0, orbitAop_08=0, smoothed_08=0, qualityInd_08=1, cno_08=0, elev_08=1, azim_08=311, prRes_08=0, chn_09=5, svid_09=17, svUsed_09=1, diffCorr_09=0, orbitAvail_09=1, orbitEph_09=1, unhealthy_09=0, orbitAlm_09=0, orbitAop_09=0, smoothed_09=0, qualityInd_09=4, cno_09=23, elev_09=26, azim_09=226, prRes_09=505, chn_10=4, svid_10=19, svUsed_10=1, diffCorr_10=0, orbitAvail_10=1, orbitEph_10=1, unhealthy_10=0, orbitAlm_10=0, orbitAop_10=0, smoothed_10=0, qualityInd_10=4, cno_10=25, elev_10=35, azim_10=242, prRes_10=1630, chn_11=6, svid_11=22, svUsed_11=1, diffCorr_11=0, orbitAvail_11=1, orbitEph_11=1, unhealthy_11=0, orbitAlm_11=0, orbitAop_11=0, smoothed_11=0, qualityInd_11=4, cno_11=21, elev_11=20, azim_11=96, prRes_11=-1033, chn_12=22, svid_12=25, svUsed_12=0, diffCorr_12=0, orbitAvail_12=1, orbitEph_12=0, unhealthy_12=0, orbitAlm_12=0, orbitAop_12=0, smoothed_12=0, qualityInd_12=1, cno_12=0, elev_12=4, azim_12=344, prRes_12=0, chn_13=11, svid_13=31, svUsed_13=1, diffCorr_13=0, orbitAvail_13=1, orbitEph_13=1, unhealthy_13=0, orbitAlm_13=0, orbitAop_13=0, smoothed_13=0, qualityInd_13=4, cno_13=14, elev_13=10, azim_13=27, prRes_13=1714, chn_14=18, svid_14=120, svUsed_14=0, diffCorr_14=0, orbitAvail_14=1, orbitEph_14=0, unhealthy_14=1, orbitAlm_14=0, orbitAop_14=0, smoothed_14=0, qualityInd_14=1, cno_14=0, elev_14=28, azim_14=196, prRes_14=0, chn_15=20, svid_15=123, svUsed_15=0, diffCorr_15=0, orbitAvail_15=1, orbitEph_15=0, unhealthy_15=1, orbitAlm_15=0, orbitAop_15=0, smoothed_15=0, qualityInd_15=1, cno_15=0, elev_15=22, azim_15=140, prRes_15=0, chn_16=16, svid_16=136, svUsed_16=0, diffCorr_16=0, orbitAvail_16=1, orbitEph_16=0, unhealthy_16=1, orbitAlm_16=0, orbitAop_16=0, smoothed_16=0, qualityInd_16=1, cno_16=0, elev_16=29, azim_16=171, prRes_16=0, chn_17=14, svid_17=65, svUsed_17=1, diffCorr_17=0, orbitAvail_17=1, orbitEph_17=1, unhealthy_17=0, orbitAlm_17=0, orbitAop_17=0, smoothed_17=0, qualityInd_17=4, cno_17=21, elev_17=33, azim_17=252, prRes_17=139, chn_18=8, svid_18=71, svUsed_18=1, diffCorr_18=0, orbitAvail_18=1, orbitEph_18=1, unhealthy_18=0, orbitAlm_18=0, orbitAop_18=0, smoothed_18=0, qualityInd_18=4, cno_18=19, elev_18=44, azim_18=53, prRes_18=1941, chn_19=9, svid_19=72, svUsed_19=1, diffCorr_19=0, orbitAvail_19=1, orbitEph_19=1, unhealthy_19=0, orbitAlm_19=0, orbitAop_19=0, smoothed_19=0, qualityInd_19=4, cno_19=20, elev_19=76, azim_19=286, prRes_19=-1155, chn_20=15, svid_20=73, svUsed_20=1, diffCorr_20=0, orbitAvail_20=1, orbitEph_20=1, unhealthy_20=0, orbitAlm_20=0, orbitAop_20=0, smoothed_20=0, qualityInd_20=6, cno_20=25, elev_20=19, azim_20=81, prRes_20=-115, chn_21=21, svid_21=79, svUsed_21=0, diffCorr_21=0, orbitAvail_21=1, orbitEph_21=0, unhealthy_21=0, orbitAlm_21=0, orbitAop_21=0, smoothed_21=0, qualityInd_21=1, cno_21=0, elev_21=0, azim_21=342, prRes_21=0, chn_22=17, svid_22=80, svUsed_22=0, diffCorr_22=0, orbitAvail_22=1, orbitEph_22=0, unhealthy_22=0, orbitAlm_22=0, orbitAop_22=0, smoothed_22=0, qualityInd_22=4, cno_22=18, elev_22=20, azim_22=29, prRes_22=0, chn_23=7, svid_23=86, svUsed_23=1, diffCorr_23=0, orbitAvail_23=1, orbitEph_23=1, unhealthy_23=0, orbitAlm_23=0, orbitAop_23=0, smoothed_23=0, qualityInd_23=4, cno_23=10, elev_23=18, azim_23=177, prRes_23=-149, chn_24=10, svid_24=87, svUsed_24=1, diffCorr_24=0, orbitAvail_24=1, orbitEph_24=1, unhealthy_24=0, orbitAlm_24=0, orbitAop_24=0, smoothed_24=0, qualityInd_24=7, cno_24=32, elev_24=65, azim_24=257, prRes_24=169, chn_25=12, svid_25=88, svUsed_25=1, diffCorr_25=0, orbitAvail_25=1, orbitEph_25=1, unhealthy_25=0, orbitAlm_25=0, orbitAop_25=0, smoothed_25=0, qualityInd_25=4, cno_25=23, elev_25=40, azim_25=318, prRes_25=-93)>",
        )
        i = 0
        raw = 0
        ubxreader = UBXReader(self.streamMIX, ubxonly=False)
        while raw is not None and i < 3:
            (raw, parsed) = ubxreader.read()
            if raw is not None:
                self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                i += 1

    def testBADHDR(self):  # invalid header in data
        EXPECTED_ERROR = "Unknown data header b'\\xb5\\x01'"
        with self.assertRaises(UBXStreamError) as context:
            i = 0
            ubxreader = UBXReader(self.streamBADHDR, True)
            for (_, _) in ubxreader:
                i += 1
        self.assertTrue(EXPECTED_ERROR in str(context.exception))

    def testBADEOF1(self):  # premature EOF after header
        i = 0
        raw = 0
        ubxreader = UBXReader(self.streamBADEOF1)
        while raw is not None:
            (raw, _) = ubxreader.read()
            i += 1
        self.assertEqual(i, 4)

    def testBADEOF2(self):  # premature EOF after message class and length
        i = 0
        raw = 0
        ubxreader = UBXReader(self.streamBADEOF2)
        while raw is not None:
            (raw, _) = ubxreader.read()
            i += 1
        self.assertEqual(i, 3)

    def testBADEOF3(self):  # premature EOF after first byte of header
        i = 0
        raw = 0
        ubxreader = UBXReader(self.streamBADEOF3)
        while raw is not None:
            (raw, _) = ubxreader.read()
            i += 1
        self.assertEqual(i, 3)

    # test parse of actual ESF-MEAS log - thanks to tgalecki for log
    # if calibTtagValid = 1; last dataField = calibTtag, numMeas = num of dataFields excluding calibTtag
    def testESFMEASLOG(
        self,
    ):
        EXPECTED_RESULT = [
            "<UBX(ESF-MEAS, timeTag=514162, timeMarkSent=0, timeMarkEdge=0, calibTtagValid=1, numMeas=3, id=0, dataField_01=16776523, dataType_01=16, dataField_02=576, dataType_02=17, dataField_03=10275, dataType_03=18, dataField_04=514162, dataType_04=0)>",
            "<UBX(ESF-MEAS, timeTag=514157, timeMarkSent=0, timeMarkEdge=0, calibTtagValid=1, numMeas=4, id=0, dataField_01=1741, dataType_01=14, dataField_02=16776932, dataType_02=13, dataField_03=16775683, dataType_03=5, dataField_04=2825, dataType_04=12, dataField_05=514157, dataType_05=0)>",
            "<UBX(ESF-MEAS, timeTag=514261, timeMarkSent=0, timeMarkEdge=0, calibTtagValid=1, numMeas=3, id=0, dataField_01=16776525, dataType_01=16, dataField_02=581, dataType_02=17, dataField_03=10271, dataType_03=18, dataField_04=514261, dataType_04=0)>",
            "<UBX(ESF-MEAS, timeTag=514256, timeMarkSent=0, timeMarkEdge=0, calibTtagValid=1, numMeas=4, id=0, dataField_01=1660, dataType_01=14, dataField_02=16776907, dataType_02=13, dataField_03=16775596, dataType_03=5, dataField_04=2825, dataType_04=12, dataField_05=514256, dataType_05=0)>",
            "<UBX(ESF-MEAS, timeTag=514360, timeMarkSent=0, timeMarkEdge=0, calibTtagValid=1, numMeas=3, id=0, dataField_01=16776522, dataType_01=16, dataField_02=577, dataType_02=17, dataField_03=10279, dataType_03=18, dataField_04=514360, dataType_04=0)>",
            "<UBX(ESF-MEAS, timeTag=514355, timeMarkSent=0, timeMarkEdge=0, calibTtagValid=1, numMeas=4, id=0, dataField_01=1551, dataType_01=14, dataField_02=16776726, dataType_02=13, dataField_03=16775771, dataType_03=5, dataField_04=2826, dataType_04=12, dataField_05=514355, dataType_05=0)>",
            "<UBX(ESF-MEAS, timeTag=514460, timeMarkSent=0, timeMarkEdge=0, calibTtagValid=1, numMeas=3, id=0, dataField_01=16776526, dataType_01=16, dataField_02=590, dataType_02=17, dataField_03=10272, dataType_03=18, dataField_04=514460, dataType_04=0)>",
            "<UBX(ESF-MEAS, timeTag=514455, timeMarkSent=0, timeMarkEdge=0, calibTtagValid=1, numMeas=4, id=0, dataField_01=1669, dataType_01=14, dataField_02=16776823, dataType_02=13, dataField_03=16775649, dataType_03=5, dataField_04=2826, dataType_04=12, dataField_05=514455, dataType_05=0)>",
            "<UBX(ESF-MEAS, timeTag=514559, timeMarkSent=0, timeMarkEdge=0, calibTtagValid=1, numMeas=3, id=0, dataField_01=16776524, dataType_01=16, dataField_02=574, dataType_02=17, dataField_03=10276, dataType_03=18, dataField_04=514559, dataType_04=0)>",
            "<UBX(ESF-MEAS, timeTag=514554, timeMarkSent=0, timeMarkEdge=0, calibTtagValid=1, numMeas=4, id=0, dataField_01=1682, dataType_01=14, dataField_02=16776801, dataType_02=13, dataField_03=16775583, dataType_03=5, dataField_04=2826, dataType_04=12, dataField_05=514554, dataType_05=0)>",
            "<UBX(ESF-MEAS, timeTag=514659, timeMarkSent=0, timeMarkEdge=0, calibTtagValid=1, numMeas=3, id=0, dataField_01=16776519, dataType_01=16, dataField_02=580, dataType_02=17, dataField_03=10268, dataType_03=18, dataField_04=514659, dataType_04=0)>",
            "<UBX(ESF-MEAS, timeTag=514654, timeMarkSent=0, timeMarkEdge=0, calibTtagValid=1, numMeas=4, id=0, dataField_01=1775, dataType_01=14, dataField_02=16776888, dataType_02=13, dataField_03=16775624, dataType_03=5, dataField_04=2826, dataType_04=12, dataField_05=514654, dataType_05=0)>",
            "<UBX(ESF-MEAS, timeTag=514758, timeMarkSent=0, timeMarkEdge=0, calibTtagValid=1, numMeas=3, id=0, dataField_01=16776522, dataType_01=16, dataField_02=590, dataType_02=17, dataField_03=10273, dataType_03=18, dataField_04=514758, dataType_04=0)>",
            "<UBX(ESF-MEAS, timeTag=514753, timeMarkSent=0, timeMarkEdge=0, calibTtagValid=1, numMeas=4, id=0, dataField_01=1666, dataType_01=14, dataField_02=16776795, dataType_02=13, dataField_03=16775624, dataType_03=5, dataField_04=2825, dataType_04=12, dataField_05=514753, dataType_05=0)>",
            "<UBX(ESF-MEAS, timeTag=514858, timeMarkSent=0, timeMarkEdge=0, calibTtagValid=1, numMeas=3, id=0, dataField_01=16776520, dataType_01=16, dataField_02=583, dataType_02=17, dataField_03=10279, dataType_03=18, dataField_04=514858, dataType_04=0)>",
            "<UBX(ESF-MEAS, timeTag=514853, timeMarkSent=0, timeMarkEdge=0, calibTtagValid=1, numMeas=4, id=0, dataField_01=1819, dataType_01=14, dataField_02=16776941, dataType_02=13, dataField_03=16775674, dataType_03=5, dataField_04=2825, dataType_04=12, dataField_05=514853, dataType_05=0)>",
            "<UBX(ESF-MEAS, timeTag=75227, timeMarkSent=0, timeMarkEdge=0, calibTtagValid=1, numMeas=4, id=0, dataField_01=630, dataType_01=14, dataField_02=16775174, dataType_02=13, dataField_03=16775134, dataType_03=5, dataField_04=2644, dataType_04=12, dataField_05=75227, dataType_05=0)>",
            "<UBX(ESF-MEAS, timeTag=74734, timeMarkSent=0, timeMarkEdge=0, calibTtagValid=1, numMeas=3, id=0, dataField_01=4584, dataType_01=16, dataField_02=2042, dataType_02=17, dataField_03=8865, dataType_03=18, dataField_04=74734, dataType_04=0)>",
            "<UBX(ESF-MEAS, timeTag=74132, timeMarkSent=0, timeMarkEdge=0, calibTtagValid=1, numMeas=4, id=0, dataField_01=1535, dataType_01=14, dataField_02=16776947, dataType_02=13, dataField_03=2893, dataType_03=5, dataField_04=2641, dataType_04=12, dataField_05=74132, dataType_05=0)>",
        ]
        for i, msg in enumerate(self.esf_meas_log):
            res = UBXReader.parse(msg, validate=VALCKSUM, parsebitfield=1)
            self.assertEqual(str(res), EXPECTED_RESULT[i])


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
