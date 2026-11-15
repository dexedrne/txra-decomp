@@ f_eff
<<<-
        events16 = gEffects[i].events;
===
        events16 = effect->events;
>>>
@@ f_eff2
<<<-
        events16 = gEffects[i].events;
===
        events16 = effect->events;
>>>
<<<-
                gEffects[i].events = 0;
===
                effect->events = 0;
>>>
@@ f_eff3
<<<-
                gEffects[i].events = 0;
===
                effect->events = 0;
>>>
@@ f_ifasg
<<<-
        events16 = gEffects[i].events;
        if (events16 != 0) {
===
        if ((events16 = gEffects[i].events) != 0) {
>>>
@@ f_ifasg2
<<<-
        events16 = gEffects[i].events;
        if (events16 != 0) {
===
        if ((events16 = gEffects[i].events)) {
>>>
@@ f_null
<<<-
                gEffects[i].events = 0;
===
                gEffects[i].events = (u16 *)0;
>>>
@@ f_e16
<<<-
                gEffects[i].events = 0;
===
                gEffects[i].events = events16 = 0;
>>>
@@ f_stopu8
<<<-
        s16 stop;
===
        u8 stop;
>>>
@@ f_stops32
<<<-
        s16 stop;
===
        s32 stop;
>>>
@@ f_stop1
<<<-
            stop = 0;

===
            stop = 0;
>>>
