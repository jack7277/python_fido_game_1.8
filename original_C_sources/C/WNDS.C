#include <conio.h>
#include <alloc.h>
#include <string.h>
#include <io.h>
#include <fcntl.h>

#define min(a,b) ((a)>(b)?(b):(a))
#define max(a,b) ((a)>(b)?(a):(b))

typedef unsigned int word;
typedef unsigned char byte;

char far *scr=(char far *)0xB8000000;
word far *scrw=(word far *)0xB8000000;
char far *low=(char far *)0x00000000;
#define loww(adr) (*(word*)(low+(adr)))
#define ctrl (low[417] & 04)

char Border[]={218,196,191,179,217,192, /*Single-Single*/
	       201,205,187,186,188,200, /*Double-Double*/
	       214,196,183,186,189,211, /*Single-Double*/
	       213,205,184,179,190,212}; /*Double-Single*/

#define SSB 0
#define DDB 6
#define SDB 12
#define DSB 18

int BRDR=SSB;

char up(unsigned char c)
{if (c>='a'&&c<='z'||c>=160&&c<=175) return c&0xDF;
 if (c>=224&&c<=239) return c-80;
 return c;
}

void prn(y,x,st) /* write string st at (y,x) */
int y,x;
char *st;
{int i=0;
if (st==NULL) return;
while (st[i]!=0)
 scr[y*160+((x+i)<<1)]=st[i++];
}

void chatr(y,x,l,c) /* change color of l symbols from (y,x) */
int y,x,l;
char c;
{int i;
 for (i=0;i<l;i++)
 scr[y*160+1+((x+i)<<1)]=c;
}

void wrt(y,x,st,n) /* write n chars of string st at (y,x) */
int y,x,n;
byte *st;
{int i=0;
while (st[i]>=15 && i<n)
 scr[y*160+((x+i)<<1)]=st[i++];
}

int wrtword(y,x,st)
int y,x;
char *st;
{int i=0;
while (st[i]!=0 && st[i]!=' ')
 scr[y*160+((x+i)<<1)]=st[i++];
return i;
}

int write(y,x,s)
int y,x;
char *s;
{int i=x,j=y;
 while (*s)
 {if (*s=='\n') {j++;i=x;} else if (*s!='\r') {scr[j*160+(i << 1)]=*s;i++;}
  s++;
 }
 return j-y+1;
}

int writen(y,x,s,n)
int y,x,n;
char *s;
{int i=x,j=y,k=0;
 while (s[k] && j<y+n)
 {if (s[k]=='\n') {j++;i=x;} else if (s[k]!='\r') {scr[j*160+(i << 1)]=s[k];i++;}
  k++;
 }
 return k;
}

void prnc(y,x,st,c) /* write string st at (y,x) in color c */
int y,x;
char *st,c;
{int i=0;
if (st==NULL) return;
while (st[i]!=0)
 {scr[y*160+(x+i)*2]=st[i];scr[y*160+(x+i++)*2+1]=c;}
}

void prncc(y,x,st,c) /* write string st at (y,x) in color c */
/* if st[i]<32 it is assumed as a new color:
   if st[i]<16, foreground = st[i]; else background=st[i]-16
   st[i]==255 means foreground = 0
*/
int y,x;
unsigned char *st,c;
{int i=0;
if (st==NULL) return;
while (st[i]!=0)
 {if (st[i]<16) c=(c & 0xF0) | st[i];
  else if (st[i]<32) c=c | (st[i] << 4);
  else if (st[i]==255) c=(c & 0xF0);
  else
  {scr[y*160+(x<<1)]=st[i];
  scr[y*160+(x++<<1)+1]=c;}
  i++;
 }
}

void clrbl(t,l,b,r,c1)
int t,l,b,r;char c1;
{int i,j;
 for(i=t;i<=b;i++)
  for (j=l;j<=r;j++)
  {scr[i*160+j*2+1]=c1;scr[i*160+j*2]=32;}
}

void _box(t,l,b,r,c1,brdr) /* write box (top,left,bottom,right) in color c1*/
/* shadow takes positions righter than r, downer than b*/
int t,l,b,r;char c1;
int brdr;
{int i,j;
 clrbl(t,l,b,r,c1);
 for (i=t+1;i<b;i++)
 { scr[i*160+l*2]=Border[brdr+3];
   scr[i*160+r*2]=Border[brdr+3];
 }
 for (i=t+1;i<=b;i++)
 { scr[i*160+(r+1)*2+1]&=7;
   scr[i*160+(r+2)*2+1]&=7;
 }
 for (i=l+1;i<r;i++)
 {scr[b*160+i*2]=Border[brdr+1];
  scr[t*160+i*2]=Border[brdr+1];
 }
 for (i=l+2;i<=r+2;i++)
  scr[(b+1)*160+i*2+1]&=7;
 scr[b*160+r*2]=Border[brdr+4];
 scr[t*160+r*2]=Border[brdr+2];
 scr[b*160+l*2]=Border[brdr+5];
 scr[t*160+l*2]=Border[brdr];
}

void box(int t,int l,int b,int r,char c)
{_box(t,l,b,r,c,BRDR);}

void *openbox(t,l,b,r,c)
int t,l,b,r;char c;
{void *q=malloc((b-t+2)*(r-l+3)*2);
 gettext(l+1,t+1,r+3,b+2,q);
 box(t,l,b,r,c);
 return q;
}

void closebox(t,l,b,r,q)
int t,l,b,r;void *q;
{puttext(l+1,t+1,r+3,b+2,q);
 free(q);
}

void block(t,b,c) /*paint screen from string t to string b*/
int t,b;
int c;   /* color */
{int i,j;
 word w=(c<<8) | (byte)'±';
 for (j=t;j<=b;j++)
  for (i=0;i<80;i++)
   scrw[j*80+i]=w;
}

int _menu(t,l,b,r,n,c1,c2,ar,hdr,h,cl,menufunc) /*return selection (from 1) or 0 on escape*/
int t,l,b,r,		/*top,left,bottom,right*/
n,                      /*number of alternatives*/
h;                      /*default selection (from 1)*/
char c1,c2;		 /* normal & selected color */
char *ar[];              /* array of alternatives */
char *hdr; 		 /* header */
char cl;		/* cl==1 => clear after select*/
void (*menufunc)(int);
{int i,j,k,sel;
 void *q;
 char c=0;
 if (!n) return 0;
 q=openbox(t,l,b,r,c1);
 prn(t,(r+l+1-strlen(hdr))>>1,hdr);
 for (i=1;i<=n;i++)
  prn(t+i,l+2,ar[i-1]);
 sel=min(h,n);
 select:
  for(i=l+2;i<r;i++) scr [(t+sel)*160+i*2+1]=c2;
 if (menufunc!=NULL) (*menufunc)(sel);
 c=getch();if (c)
 {if (sel!=n) i=sel+1; else i=1;
  while (i!=sel)
   {if (up(ar[i-1][0])==up(c))
    {for(j=l+2;j<r;j++) scr[(t+sel)*160+j*2+1]=c1;
    sel=i;break;} i==n?i=1:i++;}
 }
 switch ((int)c) {
  case 27:closebox(t,l,b,r,q);return 0;
  case 13:if (cl) closebox(t,l,b,r,q); else free(q); return sel;
  case 0:switch (c=getch()) {
   case 73:/*PgUp*/
	 if (sel>1) {for(i=l+2;i<r;i++) scr[(t+sel)*160+i*2+1]=c1;;sel=1;}
	 break;
   case 81:/*PgDn*/;
	 if (sel<n) {for(i=l+2;i<r;i++) scr[(t+sel)*160+i*2+1]=c1;;sel=n;}
	 break;
   case 72:for(i=l+2;i<r;i++) scr[(t+sel)*160+i*2+1]=c1;
	 sel==1?sel=n:sel--;break;
   case 80:for(i=l+2;i<r;i++) scr[(t+sel)*160+i*2+1]=c1;
	 sel==n?sel=1:sel++;break;
   }
  }
  goto select;
}

int menu(t,l,c1,c2,ar,hdr,h) /*return selection (from 1) or 0 on escape*/
int t,l,		/*top,left*/
h;                      /*default selection (from 1)*/
char c1,c2;		/* normal & selected color */
char *ar[];		/* NULL-terminated array of alternatives*/
char *hdr;		/* header */
{int n=0,s=0;
 while(ar[n]!=NULL) {s=max(s,strlen(ar[n]));n++;}
 s=max(s,strlen(hdr));
 return _menu(t,l,t+n+1,l+s+3,n,c1,c2,ar,hdr,h,1,NULL);
}

int menuf(t,l,c1,c2,ar,hdr,h,func) /*return selection (from 1) or 0 on escape*/
int t,l,		/*top,left*/
h;                      /*default selection (from 1)*/
char c1,c2;		/* normal & selected color */
char *ar[];		/* NULL-terminated array of alternatives*/
char *hdr;		/* header */
void (*func)(int);      /* function to call for selected strings*/
{int n=0,s=0;
 while(ar[n]!=NULL) {s=max(s,strlen(ar[n]));n++;}
 s=max(s,strlen(hdr));
 return _menu(t,l,t+n+1,l+s+3,n,c1,c2,ar,hdr,h,1,func); /*with function call*/
}

int menuncl(t,l,c1,c2,ar,hdr,h) /*return selection (from 1) or 0 on escape*/
int t,l,		/*top,left*/
h;                      /*default selection (from 1)*/
char c1,c2;		/* normal & selected color */
char *ar[];		/* NULL-terminated array of alternatives*/
char *hdr;		/* header */
{int n=0,s=0;
 while(ar[n]!=NULL) {s=max(s,strlen(ar[n]));n++;}
 s=max(s,strlen(hdr));
 return _menu(t,l,t+n+1,l+s+3,n,c1,c2,ar,hdr,h,0,NULL); /*don't clear screen*/
}

