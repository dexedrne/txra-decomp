@@ v1
<<<
                        gTempo = commands[gVoices[i].command + 1];
===
                        { u32 t = commands[gVoices[i].command + 1]; gTempo = t; }
>>>
@@ v1_tb
<<<
                        gTempo = commands[gVoices[i].command + 1];
===
                        { u32 t = commands[gVoices[i].command + 1]; gTempo = t; }
>>>
<<<
    gTempoCounter = gTempo + gTempoCounter;
===
    gTempoCounter += gTempo;
>>>
@@ v2
<<<
                        gTempo = commands[gVoices[i].command + 1];
===
                        piece = commands[gVoices[i].command + 1]; gTempo = piece;
>>>
@@ v2_tb
<<<
                        gTempo = commands[gVoices[i].command + 1];
===
                        piece = commands[gVoices[i].command + 1]; gTempo = piece;
>>>
<<<
    gTempoCounter = gTempo + gTempoCounter;
===
    gTempoCounter += gTempo;
>>>
@@ v3
<<<
                        gTempo = commands[gVoices[i].command + 1];
===
                        { u32 t; t = commands[gVoices[i].command + 1]; gTempo = t; }
>>>
@@ v3_tb
<<<
                        gTempo = commands[gVoices[i].command + 1];
===
                        { u32 t; t = commands[gVoices[i].command + 1]; gTempo = t; }
>>>
<<<
    gTempoCounter = gTempo + gTempoCounter;
===
    gTempoCounter += gTempo;
>>>
@@ v4
<<<
                        gTempo = commands[gVoices[i].command + 1];
===
                        { s32 t = commands[gVoices[i].command + 1]; gTempo = t; }
>>>
@@ v4_tb
<<<
                        gTempo = commands[gVoices[i].command + 1];
===
                        { s32 t = commands[gVoices[i].command + 1]; gTempo = t; }
>>>
<<<
    gTempoCounter = gTempo + gTempoCounter;
===
    gTempoCounter += gTempo;
>>>
@@ v5
<<<
                        gTempo = commands[gVoices[i].command + 1];
===
                        gain = commands[gVoices[i].command + 1]; gTempo = gain;
>>>
@@ v5_tb
<<<
                        gTempo = commands[gVoices[i].command + 1];
===
                        gain = commands[gVoices[i].command + 1]; gTempo = gain;
>>>
<<<
    gTempoCounter = gTempo + gTempoCounter;
===
    gTempoCounter += gTempo;
>>>
@@ v6
<<<
                        gTempo = commands[gVoices[i].command + 1];
===
                        j = commands[gVoices[i].command + 1]; gTempo = j;
>>>
@@ v6_tb
<<<
                        gTempo = commands[gVoices[i].command + 1];
===
                        j = commands[gVoices[i].command + 1]; gTempo = j;
>>>
<<<
    gTempoCounter = gTempo + gTempoCounter;
===
    gTempoCounter += gTempo;
>>>
