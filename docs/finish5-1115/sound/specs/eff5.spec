@@ k_noeff
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
===
    for (i = 0; i <= 3; i++) {
>>>
@@ k_noeff2
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
===
    for (i = 0; i <= 3; i++) {
>>>
<<<
    Effect *effect;
===
>>>
@@ k_effinc
<<<
    for (i = 0; i <= 3; effect++, i++) {
===
    for (i = 0; i <= 3; i++, effect++) {
>>>
@@ k_effpre
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
===
    for (i = 0, effect = gEffects; i <= 3; effect++, i++) {
>>>
