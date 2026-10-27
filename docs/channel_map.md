# SEED 62-Channel Map & Brain Regions

0-based channel index used by `KEEP_CHANNELS`:

FP1(0) FPZ(1) FP2(2) AF3(3) AF4(4) F7(5) F5(6) F3(7) F1(8) FZ(9)
F2(10) F4(11) F6(12) F8(13) FT7(14) FC5(15) FC3(16) FC1(17) FCZ(18) FC2(19)
FC4(20) FC6(21) FT8(22) T7(23) C5(24) C3(25) C1(26) CZ(27) C2(28) C4(29)
C6(30) T8(31) TP7(32) CP5(33) CP3(34) CP1(35) CPZ(36) CP2(37) CP4(38) CP6(39)
TP8(40) P7(41) P5(42) P3(43) P1(44) PZ(45) P2(46) P4(47) P6(48) P8(49)
PO7(50) PO5(51) PO3(52) POZ(53) PO4(54) PO6(55) PO8(56) CB1(57) O1(58) OZ(59)
O2(60) CB2(61)

## Emotion relevance by region
- Prefrontal / Frontal (FP1, FP2, F3, F4, F7, F8 ...): HIGH — frontal asymmetry encodes valence
- Temporal (T7, T8, FT7, FT8): HIGH — emotional processing; key for 2-channel
- Central / Parietal: medium-low
- Occipital (O1, Oz, O2): LOW — mainly visual (used as control)

## Consumer device reference
- Muse: 4 ch — AF7, AF8 (forehead) + TP9, TP10 (behind ears / near temporal)
- Emotiv Insight: 5 ch — AF3, AF4, T7, T8, Pz
- NeuroSky: 1 ch (frontal)

The frontal+temporal positions favored here align with Muse's successful design.
