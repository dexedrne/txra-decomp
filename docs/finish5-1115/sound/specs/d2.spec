@@ p_command
<<<-
p = gVoices[i].pitch; p += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = p;
===
command = gVoices[i].pitch; command += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = command;
>>>
@@ p_j
<<<-
p = gVoices[i].pitch; p += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = p;
===
j = gVoices[i].pitch; j += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = j;
>>>
@@ p_cidx
<<<-
p = gVoices[i].pitch; p += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = p;
===
cidx = gVoices[i].pitch; cidx += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = cidx;
>>>
