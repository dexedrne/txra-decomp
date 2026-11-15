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
@@ p_gain
<<<-
p = gVoices[i].pitch; p += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = p;
===
gain = gVoices[i].pitch; gain += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = gain;
>>>
@@ p_piece
<<<-
p = gVoices[i].pitch; p += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = p;
===
piece = gVoices[i].pitch; piece += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = piece;
>>>
@@ p_marker
<<<-
p = gVoices[i].pitch; p += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = p;
===
marker = gVoices[i].pitch; marker += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = marker;
>>>
@@ p_none
<<<-
p = gVoices[i].pitch; p += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = p;
===
gVoices[i].pitch += slide[gVoices[i].pitch_cursor];
>>>
@@ p_none2
<<<-
p = gVoices[i].pitch; p += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = p;
===
gVoices[i].pitch = gVoices[i].pitch + slide[gVoices[i].pitch_cursor];
>>>
@@ p_local
<<<-
p = gVoices[i].pitch; p += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = p;
===
{ s32 p = gVoices[i].pitch; p += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = p; }
>>>
@@ p_local2
<<<-
p = gVoices[i].pitch; p += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = p;
===
{ s32 q = gVoices[i].pitch; q += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = q; }
>>>
@@ p_sum
<<<-
p = gVoices[i].pitch; p += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = p;
===
p = gVoices[i].pitch + slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = p;
>>>
