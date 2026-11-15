/* Partial recovery of 08002854, through 080029F0 only. Not a replacement.
 * The full streaming owner still needs its geometry-generation branches.
 * Coordinates, output records and active flags use the existing 28/56-byte
 * layouts; no machine registers or fabricated frame padding are represented. */
typedef signed int s32;
typedef unsigned short u16;
typedef struct { s32 x,y,z,active,sx,sy,depth; } StreamPoint;
typedef struct {
    u16 active,flags;
    s32 corner[4],u[4],v[4];
    u16 texture,tail;
} StreamQuad;
typedef struct {
    s32 current,next,next2,previous2,previous,slot;
} StreamWindow;
void recover_streaming_window(s32 reverse,s32 position,s32 count,s32 ring,
                              StreamPoint *points,StreamQuad *quads,StreamWindow *w)
{
    s32 i;
    if (!reverse) {
        w->current=position+28;
        if (w->current>=count) w->current-=count;
        w->slot=ring;
    } else {
        w->current=position-1;
        if (w->current<0) w->current+=count;
        w->slot=(ring-29)&31;
    }
    w->next=w->current+1;
    if (w->next>=count) w->next=0;
    w->next2=w->next+1;
    if (w->next2>=count) w->next2=0;
    w->previous2=w->current-2;
    if (w->previous2<0) w->previous2+=count;
    w->previous=w->current-1;
    if (w->previous<0) w->previous+=count;
    points+=(w->slot&31)*24;
    quads+=(w->slot&31)*24;
    for (i=23;i>=0;i--) {
        points->active=0;
        quads->active=0;
        points++;
        quads++;
    }
}
