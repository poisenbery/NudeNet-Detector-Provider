SEGGSMaster is a pun on the SEGS data type and the colloquial misspelling of "Sex" as "seggs."
Node is found under Impact Pack with the other Detector Providers.

Bethesda version of NudeNet V3 detector provider to work with Impact Pack ComfyUI.
KNOWN ISSUES:
1.)Dilate does not work. It will give an error and I do not know how any of this works.
   If you want dilate mask, use segs to mask -> dilate mask -> mask to segs
2.) Threshold filtering is buggy. I do not know the conditions to replicate the issue. The Nudenet.py already filters things below .25 so keep it at .25 just to be safe. I'll eventually get around to fixing these bugs. You can make an issue if you want, but be aware that I already know about these things, I'm just not smart enough to know how to fix them because 90% of this code is taken from other sources.


This is a very crude attempt and can 100% be made better by someone with actual programming experience.


Labels for filter: 
```
    "FEMALE_GENITALIA_COVERED",
    "FACE_FEMALE",
    "BUTTOCKS_EXPOSED",
    "FEMALE_BREAST_EXPOSED",
    "FEMALE_GENITALIA_EXPOSED",
    "MALE_BREAST_EXPOSED",
    "ANUS_EXPOSED",
    "FEET_EXPOSED",
    "BELLY_COVERED",
    "FEET_COVERED",
    "ARMPITS_COVERED",
    "ARMPITS_EXPOSED",
    "FACE_MALE",
    "BELLY_EXPOSED",
    "MALE_GENITALIA_EXPOSED",
    "ANUS_COVERED",
    "FEMALE_BREAST_COVERED",
    "BUTTOCKS_COVERED",
```
