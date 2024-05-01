/*
Исходники игры FIDO v. 1.8. 
Автор - Юрий Нестеренко
URL: http://yun.complife.net
e-mail: comte@au.ru
При внесении любых модификаций указание моих копирайтов обязательно
*/


typedef unsigned int word;
typedef unsigned char byte;
typedef unsigned long dword;

#include <stdio.h>
#include <stdlib.h>
#include <dos.h>
#include "\c\wnds.c"
#include "date.cpp"
#define salloc(x) (char *)malloc((x+1))
#define abs(x) ((x)<0?-(x):(x))
#define _rnd(x) (((dword)rand()*(x))/(RAND_MAX+1))
dword lrandom(dword x)
{return x?(_rnd(0xFFFFL)*_rnd(0xFFFF) % x):0;}
#define random_(x) ((x)<0?-_rnd(-(x)):_rnd((x)))
#define upcase(c) (((c)>='a' && (c)<='z')?(c)& ~0x20:(c))
#define setbit(x,n) ((x)|=1 << (n))
#define tstbit(x,n) ((x) & (1 << (n)))


char *status[]={"Юзер","Поинт","Нод","NC"};
char *profn[]={"---","Программирование","Железо","Торговля/менеджмент",NULL};
char *stper[]={"СЕССИЯ!","Семестр","Каникулы"};
word bps[]={2400,9600,14400,21600,28800,33600};  
char *comp[]={"286","386DX40","486DX2/66","486DX100","Pentium-133","Pentium-166","Pentium Pro 200"};
word hd[]={20,40,120,540,850,1200,2500};  /*  Объемы жесткого диска в МБ  */
int mprice[]={5,50,100,180,240,350};  /*  Цены на модем в $  */
int cprice[]={45,140,350,550,800,1000,2300};  /*  Цены на компьютеры в $  */
int hprice[]={5,10,40,80,120,200,300};  /*  Цены на HDD, в $  */
char *pref="MO.\x00     ";
char *echoname[]={"NETMAIL","LOCAL.PVT","*POINT","PVT.EXCH.COMPUTER","PVT.EXCH.BLACK.LOG",
		  "RU.ANEKDOT","*JOB","VERY.COOL","SU.HARDW","SU.SOFTW","файлэхи",
		  NULL,NULL,NULL,NULL,NULL,NULL};
char *echodescr[]={"Личная почта","Локалка","Поинтовые дела","Покупка/продажа железа","Что у кого стоит покупать",
		   "Анекдоты","Устройство на работу","Весьма полезная эха","Тонкости железа","Программирование",
		   NULL, "Моя крутая эха #1            ","Моя крутая эха #2            ","Моя крутая эха #3            ","Моя крутая эха #4            ","Моя крутая эха #5            "};
char *bbsnames[]={
"Format complete",
"Ctrl-Alt-Del",
"Fatal error",
"Exception 13",
"NO CARRIER",
"Lamer Hunter",
"Windows Must Die",
"Beer Club",
"Mailoman's",
"Crazy Gamers",
NULL,
"                  "};
char *cityname[23];
struct {
 char *name;
 char *pref;
 char frnds;
 int fr;
} cities[]={
 {"Москва","MO.",0,0},
 {"Санкт-Петербург","SPB.",0,0},
 {"Владивосток","VL.",0,0},
 {"Днепропетровск","DN.",0,0},
 {"Донецк","DONBASS.",0,0},
 {"Екатеринбург","MU.",0,0},
 {"Иркутск","ESIB.",0,0},
 {"Калуга","KLG.",0,0},
 {"Киев","KIEV.",0,0},
 {"Краснодар","KR.",0,0},
 {"Красноярск","KRS.",0,0},
 {"Луганск","LUG.",0,0},
 {"Нижний Тагил","NT.",0,0},
 {"Новокузнецк","NKZ.",0,0},
 {"Новосибирск","NSK.",0,0},
 {"Пермь","PERM.",0,0},
 {"Псков","PSKOV.",0,0},
 {"Рязань","RZ.",0,0},
 {"Томск","TSK.",0,0},
 {"Уфа","UFA.",0,0},
 {"Харьков","KHARKOV.",0,0},
 {"Челябинск","CHEL.",0,0}
};

char *style[]={"Read-only", "Неактивный", "Активный", "Flame",NULL};
int prob[]={0,1,4,8}; //вероятность [+] в % как f(Style) при izverg==1
Date lstscn;
int newdayf=0;
#define LE 10
byte BBSf;
Date D,SD;
int E=LE+1;
int Stable=0;
int Log=0;
int Style=0;
int LastBBS=0;
int pluses=0,newm=0,newc=0,newh=0;
dword alltime=0;
int Time=0,Down=0;
int City=0;
int maxpnt=0;
int auto_[]={0,0,0,0}; //link, debt, OS, antivirus

struct person {
 char *name;
 byte status;
 byte sysop;
 byte modem,comp,hd;
 int mreli,creli,hreli;
 int income,expens;
 int spay;       //pay for study
 long money,debt;
 dword soft;
 byte os,osreq;
 dword hdspace;
 byte virus;
 int ftime,wtime; //minutes
 int wdays;
 int sdays; //days of study; -1 - wait for 1.09
 byte wprof;
 byte sprof; //work & study profile
 int mood; //%
 int tired;
 int reput;
 int moder;
 int points;
 int friends;
 Date antiv;
 Date wdate;
 Date grad; //graduation date
 byte tries; //of entering
 byte army;  // 3-военнобязанный 1-студент 2-временная отмазка 0-постоянная
 int intens;
 float mark; //средний балл
 byte echo[5];
 int skill[4];//0,prg,hrd,trd;
 int reput_();
} you={salloc(31),0,0,0,0,0,32767,32767,32767,0,-150,0,300,0,0,0,0,20*1024,0,20*60,0,0,0,0,0,60,0,0,0,0,0,0,0,0,0,2,100,0.0};

int person::reput_()
{return reput+skill[1]+skill[2]+skill[3];}

struct {
 char *name;
 int mxtime;  //-1 means twit, 0 - 1st time
 int time;    //current time
 long U,D;    //upload,download
 dword soft;   //total not-your soft
 byte modem;
 byte down;
 byte ech[LE-2];
} bbs[10];

typedef struct {
 long size;
 byte itime;
 byte mincomp;
} OS;

void mailtime();
void worktime();
void studtime();
void joytime();

typedef struct {
 char *name;
 int ord;
 void (*func)();
} toccup;

toccup occup[]={{"Почта      ",1,mailtime},{"Работа     ",2,worktime},{"Учеба      ",3,studtime},{"Развлечения",4,joytime}};

char *OSnames[]={
"MSDOS 5.0",
"MSDOS+Win'3.11",
"Windows 95",
"Windows NT",
"OS/2",
"Linux",
NULL};

OS os[]={
{3L<<10,8,0},
{15L<<10,20,1},
{70L<<10,30,2},
{100L<<10,60,3},
{150L<<10,50,3},
{200L<<10,90,3}};

typedef struct  {
 char *qstn;
 char *ans[3];
 byte mark;
 byte correct;
} question;

question qstns[]=
{{"Каково время ZMH зоны 2?",
 {"2:30 - 3:30 UTC","3:30 - 4:30 UTC","5:30-6:30 московского времени"},
 0,0},
 {"Что обязан делать нод?",
 {"Набирать поинтов", "Поддерживать ZMH", "Раздавать файлэхи"},
 0,1},
 {"Что означают цифры 5020 в адресе 2:5020/1402?",
 {"Номер зоны","Номер статьи УК","Номер сети"},
 0,2},
 {"Вправе ли нод просматривать нетмэйл, идущий\n через его узел?",
 {"Да","Нет","Не только просматривать, но и изменять"},
 0,0},
 {"Для чего предназначен ZMH?",
 {"Для работы ББС","Для пересылки нетмэйла","Для отдыха сисопа"},
 0,1},
 {"Какова плата за подключение к ФИДО?",
 {"$50","3 бутылки пива", "Подключение бесплатное"},
 0,2},
 {"Кто осуществляет управление сетью?",
 {"Координатор", "Администратор", "Модератор"},
 0,0},
 {"Каким образом получает должность Координатор \nЗоны?",
 {"Жеребьевкой", "Голосованием", "По наследству"},
 0,1},
 {"При возникновении конфликта с другим сисопом \nпервым делом надо:",
 {"Подать жалобу сетевому координатору","Подать в суд","Попытаться решить конфликт нетмэйлом"},
 0,2}
};

typedef struct {
 char *str;
 byte mark,correct;
} list;

list ndreq[]={
 {"Ваше имя",0,1},
 {"Возраст",0,0},
 {"Пол",0,0},
 {"Семейное положение",0,0},
 {"Город и страна, где расположена стация",0,1},
 {"Домашний адрес",0,0},
 {"Номер голосового телефона",0,1},
 {"Место работы",0,0},
 {"Годовой доход",0,0},
 {"Образование",0,0},
 {"Номер модемного телефона",0,1},
 {"Название вашей станции",0,1},
 {"Ваш компьютер",0,0},
 {"Ваш модем",0,1},
 {"Стаж работы с компьютером",0,0},
 {"Время работы вашей станции",0,1},
 {"Национальность",0,0},
 {"Партийная принадлежность",0,0},
 {"BPS вашего модема",0,1},
 {"Каким мэйлером пользуетесь",0,1},
 {"Привлекались ли к уголовной ответственности",0,0}
};

struct echo {
 char *name;
 byte stat; //0 - Unlinked 1 - Linked 2 - moderator 80 - read from BBS
 byte mark; //1 - autoread, 2 - passthru
 int msg,newm,new1; //messages: total, unread, new for this day
 Date dl; //для отключенных - дата подключения. if < current - ignored
 byte plus; //number of [+]
 int traf; //средний трафик в К
 float trafk; //traf*trafk - сколько мин. в день отнимает чтение эхи (Style==0)
 int read; // % свежих прочитанных писем, за 4 дня уходит в 0
 float izverg; //коэф. злобности модератора
 int moderatorial(int y=5,int x=8);
 virtual int event() {return 0;}
 echo(int n);
};

echo *echoes[LE+6];

FILE *log,*errlog;
void elog(char *s)
{errlog=fopen("errlog","a+t"); fprintf(errlog,"%s %lu\n",s,coreleft());fclose(errlog);}

void delay (word ms)
  /* Точная процедура ожидания */
{
if (you.os) ms>>=2;
asm {
   mov   CX, ms
   jcxz   l3
   }
   /* Берем в DX 1-й отсчет таймера */
   l1:
 asm {
   mov   AL, 4
   out   43h, AL
   In   AL, 40h
   mov   DL, AL
   nop
   In   AL, 40h
   mov   DH, AL
   }
   l2:
 asm {
   /* Берем в AX 2-й отсчет таймера */
   mov   AL, 4
   out   43h, AL
   In   AL, 40h
   mov   AH, AL
   nop
   In   AL, 40h
   xchg   AL, AH
   mov   BX, DX
   sub   BX, AX
   cmp   BX, 1160 * 2
   jb   l2
   loop   l1
   }
   l3:return;
}

int studper(Date D)
{if (D<25.01 || D>=1.06 && D<25.06) return 0; //session
 else if (D>=1.09 || D>=6.02 && D<1.06) return 1; //semestr
 else return 2;//vacations
}

#define echtime(i) round(echoes[(i)]->traf*echoes[(i)]->trafk*(Style+1)*(echoes[(i)]->stat>2?1:echoes[(i)]->stat)*(11.0-you.comp/1.5)*(you.os>0?1:1.3)/10.0)
int sttime()
{if (!you.spay) return 0;
 else if (you.spay<0)
  return studper(D)==2?0:6*60.0*you.intens/100.0;
 else return 2*60;
}

int echtime1(i,n)
{int t=round((n)*2*echoes[i]->trafk*(Style+1)*(echoes[i]->stat>2?1:echoes[i]->stat)*(11.0-you.comp/1.5)*(you.os>0?1:1.3)/10.0);
 if (!t && n) t=1;
 return t;
}

echo::echo(int n)
{if (echoname[n]==NULL)
 {echoname[n]=salloc(30);echoname[n][29]=0;memset(echoname[n],' ',29);}
 name=echoname[n];
 stat=plus=0;dl=0;
 izverg=1;traf=20;trafk=0.4;read=0;
 newm=0;msg=0;mark=0;
}


void delecho(int n)
{int i;
 if(n>LE) {E--;you.moder--;free(echoes[n]->name);}
 delete echoes[n];
 for (i=n;i<E;i++)
 {echoes[i]=echoes[i+1];
  echoname[i]=echoname[i+1];echoes[i]->name=echoname[i];
  echodescr[i]=echodescr[i+1];
 }
 if (n>LE) echoname[E]=NULL;
}

struct netmail:echo {
 int event();
 netmail();
};

netmail::netmail():echo(0)
{izverg=0;traf=0;trafk=0.7;}

struct local:echo {
 int event();
 local();
};

local::local():echo(1)
{izverg=0;traf=10;trafk=0.5;}

struct point:echo {
 int event();
 point();
};

point::point():echo(2)
{traf=15;
}

struct exch:echo {
 int event();
 exch();
};

exch::exch():echo(3) {}

struct bllog:echo {
 int event();
 bllog();
};

bllog::bllog():echo(4) {}

struct ruanekdot:echo {
 int event();
 ruanekdot();
};

ruanekdot::ruanekdot():echo(5)
{izverg=4;traf=70;trafk=0.5;
}

struct job:echo {
 int event();
 job();
};

job::job():echo(6)
{izverg=2.0;traf=35;trafk=0.2;}

struct vcool:echo {
 int event();
 vcool();
};

vcool::vcool():echo(7)
{izverg=2.0;traf=45;trafk=0.45;}

struct hardw:echo {
 int event();
 hardw();
};

hardw::hardw():echo(8)
{traf=100;trafk=0.4;}

struct softw:echo {
 int event();
 softw();
};

softw::softw():echo(9)
{traf=100;trafk=0.4;}

struct fecho:echo {
 int event();
 fecho();
};

fecho::fecho():echo(10)
{izverg=0;traf=1024;trafk=0.01;}

word Cursor;

void cursoff()
{if (loww(0x460)!=0x2000)
 {Cursor=loww(0x460);
  asm  {
   mov ax,0100h
   mov cx,2000h
   int 10h
  }
 }
}

void curson()
{asm {
  mov ax,0100h
  mov cx,Cursor
  int 10h
 }
}

//graphics

typedef struct {
 char signat[2];
 long fsize;
 int rsrvd[2];
 long offset;
 long hlen;
 long width;
 long height;
 int planes;
 int bpp;
 long compress;
 long imglen;
 long xres;
 long yres;
 long colors;
 long maincols;
} bmphdr;

char far *screen=(char far*)0xA0000000L;

int setvesa640x480x256(void)
{word res;
asm{
  mov ax,4f02h
  mov bx,101h
  int 10h
  mov res,ax
  }
  return res==0x4f;
}

void textmode()
{asm{
     mov ax,03h
     int 10h
     }
}

void setbank(int bank) // Hадеюсь ты знаешь что такое банк? ;-)
{
asm{
   mov ax,4f05h
   mov bx,0
   mov dx,bank
   push dx
   int 10h
   mov bx,1
   pop dx
   int 10h
   }
}

void setbmpal(byte far *addr,int palsz)
{
asm {   push ds
        mov cx,palsz
        shr cx,2
        dec cx
        std
        lds si,addr     ;указатель на конец палитры
     }
nxtcol:
asm     {
        mov al,cl
        mov dx,3c8h
        out dx,al
        inc dx
        lodsb
        lodsb
        shr al,2
        out dx,al
        lodsb
        shr al,2
        out dx,al
        lodsb
        shr al,2
        out dx,al
        jcxz all
        dec cl
        jmp nxtcol
}
all:
asm {
        pop ds
    }
}

long min_(long *x,long y)
{
  if (*x < y)
  {
    y = *x;
    *x = 0;
    return y;
  }
  *x -= y;
  return y;
}

int loadbmp(char *name,byte **where)
{bmphdr h1;
 byte* buf;
 int palsz,f,j,i;
 long size;
 if ((f=open(name,O_RDONLY|O_BINARY))==-1) return 0;
 read(f,&h1,14+40);
 if (*(int*)h1.signat!=0x4D42 || h1.compress) return -1;
 palsz=h1.offset-14-40;
 *where=(byte*)malloc(h1.offset);
 memmove(*where,&h1,14+40);
 read(f,(*where)+14+40,palsz);
 setbmpal((*where)+14+40+palsz-1,palsz);
 if ((buf=(byte*)malloc(min(32768L,size=h1.imglen)))==NULL) return -2;
 for (j=0;j<5;j++)
 {setbank(j);
  i=read(f,buf,min_(&size,32768));
  memmove(screen,buf,i);
  if (size<=0) break;
  i=read(f,buf,min_(&size,32768));
  memmove(screen+32768,buf,i);
  if (size<=0) break;
 }
// for (i=h1.height;i;i--) memmove(screen+640*i,h1.width)
 free(buf);
 close(f);
 return 1;
}

/*void scrlup(char t,char l,char b,char r,char c,char n=1)
{asm {
 mov ah, 06
 mov al, n
 mov bh,c
 mov ch,t
 mov cl,l
 mov dh,b
 mov dl,r
 int 10h
 }
}

void scrldn(char t,char l,char b,char r,char c,char n=1)
{asm {
 mov ah, 07
 mov al, n
 mov bh,c
 mov ch,t
 mov cl,l
 mov dh,b
 mov dl,r
 int 10h
 }
}
*/
void quit(int i)
{fclose(log);curson();clrscr();exit(i);}

int input(char *s0,byte l) //return 0 if Esc was pressed -> s0 not changed
{signed char  i,j,p,l1=strlen(s0);
 char *s;
 char c;
 s=strdup(s0);curson();
 c=getch();
 if (c && c!=13 && c!=27)
 {cursoff();
  for (i=0;i<l;i++) putch(32);
  for (i=0;i<l;i++) putch(8);
  s[0]=p=0;
  curson();
 } else p=l1;
 i=0;
 while (c!=13 && c!=27) {
  switch (c) {
   case 0:
    c=getch();
    switch (c) {
    case 75:if (i>0) {i--;putch(8);} break;
    case 77:if (i+1<min(p,l)) {putch(s[i]);i++;} break;
    case 82:cursoff();putch(32);                      /* ins */
      for (j=min(p-1,l-1);j>i;j--) s[j]=s[j-1];
      s[i]=' ';
      if (p<l) p++;
      for (j=i+1;j<p;j++) putch(s[j]);
      for (j=p;j>i;j--) putch(8);
      curson();break;
    case 83:cursoff();                               /* del */
      for (j=i+1;j<p;j++) {s[j-1]=s[j];putch(s[j]);};
      putch(32);for (j=p;j>i;j--) putch(8);
      if (i<p-1) p--; else s[i]=' ';
      curson();
    } break;
  case 8:if (i>0)  {i--;cursoff();putch(8);
    for (j=i+1;j<p;j++) {s[j-1]=s[j];putch(s[j]);};
    putch(32);for (j=p;j>i;j--) putch(8);p--;
    curson();} break;
//  case 32:
  default:
//   if ((c>='A' && c<='z') || (c>='0' && c<='9') || c=='.' || c==' ')
//  if ((c>='A') || (c>='0' && c<='9'))
   {putch(c);s[i]=c;
    if (i>=p) p++;if (i<l-1) i++; else putch(8);
    }
  }
  if (c!=13 && c!=27) c=getch();
 }
 if (c!=27) {while (p && s[--p]==' ');s[p+1]=0;strcpy(s0,s);} else
 {
  for (j=i-1;i>=1;i--) putch(8);
  for (i=0;i<l1;i++) putch(s0[i]);
  for (i=0;i<(l-l1);i++) putch(32);
 }
 cursoff();free(s);
 return (c!=27);
}

#define gotoyx(y,x) gotoxy((x)+1,(y)+1)
#define ESC (kbhit() && getch()==27)
#define scrs(y,x,c) (scr[(y)*160+((x)<<1)]=(c))
#define scra(y,x,c) (scr[(y)*160+((x)<<1)+1]=(c))
#define scrsa(y,x,w) (scrw[(y)*80+(x)]=(w))

void anykey()
{void *q=malloc(160);
 gettext(1,25,80,25,q);
 prnc(24,0,"                              Нажмите клавишу \"Anykey\"                         ",0x74);
 if (!getch()) getch();
 puttext(1,25,80,25,q);
 free(q);
}

void viewstr(char *s,int t=2,int l=5,int h=20,int w=70, char col=0x70)
{int p=0,p1,i;
 char c;
 void *q=openbox(t,l,t+h,l+w,col);
 show:clrbl(t+1,l+2,t+h-1,l+w-1,col);
 p1=writen(t+1,l+2,s+p,h-1);
 do
 switch (c=getch()) {
  case 27:goto all;
  case 0:switch (c=getch()) {
   case 73:/*PgUp*/
	 for(i=0;i<h-1;i++)
	  {if (!p) break; p--;
	   while (p) {p--;if (s[p-1]=='\n') break;}} goto show;
   case 72:if (!p) break; p--;
	   while (p) {p--;if (s[p-1]=='\n') break;}
	   goto show;
   case 81:/*PgDn*/
	 for(i=0;i<h-1;i++)
	  while (s[p]) {p++;if (s[p-1]=='\n') break;} goto show;
   case 80:while (s[p]) {p++;if (s[p-1]=='\n') break;}
	  goto show;
   }
  }
  while (1);
  all:
  closebox(t,l,t+h,l+w,q);
}

void message(char *s,char c,int wait=1,int y=0xFF,int x=0)
{int i=0,k=0,l=0,n=1;
 void *q;
 while (s[i]) if (s[i++]=='\n') {if (k>l) l=k; k=0;n++;} else k++;
 if (k>l) l=k;
 if (y==0xFF) //center
 {y=(25-n) >> 1;
  x=(76-l) >> 1;
 }
 q=openbox(y,x,y+n+1,x+l+3,c);
 write(y+1,x+2,s);
 if (Log) fprintf(log,"%d.%d.%d\n%s\n",D.day(),D.month(),D.year(),s);
 switch (wait)
 {case 1: anykey();closebox(y,x,y+n+1,x+l+3,q);break;
  case 0:free(q);break;
  default:delay(1000);closebox(y,x,y+n+1,x+l+3,q);break;
 }
}

int nmbrscrl(int *n,int y,int x,int mx=99,int mn=0,int dn=1)
{char c=0,s[8];
 int r=*n;
 register int d;
 if (r<mn) r=mn; else if (r>mx) r=mx;
 sprintf(s,"%3d",r);prn(y,x+1,s);
 scrs(y-1,x,30);scrs(y+1,x,31);scrs(y,x,'■');
 while ((c=getch())!=27)
 {switch (c) {
   case 0:continue;
   case 80:if (r>=mn+dn) r-=dn;break;
   case 72:if (r<=mx-dn) r+=dn;break;
   case 13:d=r-*n;*n=r;return d;
  }
  sprintf(s,"%3d",r);prn(y,x+1,s);
 }
 return 0;
}

char *week[]={"Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"};
char *month[]={"Январь","Февраль","Март","Апрель","Май","Июнь","Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь",NULL};
char *situat[]={"Нестабильная","Стабильная",NULL};

char *dtm=salloc(40);
void showtime()
{sprintf(dtm,"%11s, %02d.%02d.%d  Осталось %d ч. %02d мин. ",week[D.weekday()],D.day(),D.month(),D.year(),Time/60,Time%60);
 prnc(0,32,dtm,Time>=6*60?0x1F:0x1C);
}

void showhelp()
{char *s=salloc(160);
 sprintf(s," \x04G\xFF\x61me │\x04 B\xFF\x42S  \x04U\xFFpgrade  \x04J\xFF\ob  \x04L\xFF\earn  \x04S\xFFoft  %cE\xFF\choes  %cP\xFFoints  %cF\xFFriends  \x04T\xFFime  \x04N\xFF\ext day        ",
	 you.status?'\x04':'\xFF',you.status>1?'\x04':'\xFF',you.friends?'\x04':'\xFF');
 prncc(24,0,s,0x70);
 free(s);
}

char *end1[]={"","а","ов"};
char *end2[]={"день","дня","дней"};

char *end(dword x,char** ending=end1)
{if (x<=20 && x>10) return(ending[2]);
 x=x%10-1;
 return(x<4?(x?ending[1]:ending[0]):ending[2]);
}

#define mtok(x) ((x)<<10)
#define BB() ((dword)you.hdspace<mtok((long)hd[you.hd]))


void showstat(int y=1,int x=22,char c=0x30,char c2=0x3F)
{char *mood[]=
{"==8~-(E (","=8~-((","8~-(",":~-(",":-(",":-/",":-I",";-I",";-)",":-)",
 "Ж:-)","Ж:-))","Ж8-D","Ж|-))","Ж|-)))","Ж|-)))"};
 char *s=salloc(50);
 word i;
 _box(y,x,y+17+you.sysop+you.moder,x+55,c,SDB);
 prnc(y+1,x+2,you.name,c2);
 prn(y+2,x+2,"Статус: ");prnc(y+2,x+11,status[you.status],c2);
 if (you.status>1)
 {sprintf(s,"(%d поинт%s)",you.points,end(you.points));
  prnc(y+2,x+17,s,c2);
 }
 if (you.sysop)
 {y++;i=sprintf(s,"Сисоп %c%s BBS ",c2&0xF,bbsnames[11]);
  if (Down || you.modem==0xFF) sprintf(s+i,"\x04(в дауне)");
  else sprintf(s+i,"(требует ~%d мин.в день)",round(75*(you.modem+1)*.1+10));
  prncc(y+2,x+2,s,c);
 }
 for (i=0;i<you.moder;i++)
 {prn(y+3+i,x+3,"Модератор ");prnc(y+3+i,x+3+10,echoes[LE+1+i]->name,c2);}
 y+=you.moder;
 sprintf(s,"Репутация: %c%d",c2&0xF,you.reput);
 prncc(y+3,x+2,s,c);
 if ((you.comp | you.modem)==0xFF) prnc(y+4,x+2,"Проблемы с hardware!",c2);
 else
 {sprintf(s,"Компьютер %c%s\xFF  Модем на %c%u",c2&0xF,comp[you.comp],c2&0xF,bps[you.modem]);
  prncc(y+4,x+2,s,c);
 }
 i=sprintf(s,"Винт %c%dМ ",c2&0xF,hd[you.hd]);
 if (BB())
  i+=sprintf(s+i,"\x04%luК в бэд блоках%c",((dword)hd[you.hd]<<10)-you.hdspace,c2&0xF);
 sprintf(s+i," %luK free",you.hdspace-you.soft-os[you.os].size);
 prncc(y+5,x+2,s,c);
 for (i=1;i<=3;i++)
 {sprintf(s,"%s %c%d",profn[i],c2&0xF,you.skill[i]);prncc(y+5+i,x+2,s,c);}
 sprintf(s,"Работа:%c%s\xFF З/п %c$%d\xFF Стаж %c%d д.",c2&0xF,profn[you.wprof],c2&0xF,you.income,c2&0xF,you.wdays);
 prncc(y+9,x+2,s,c);y++;
 i=sprintf(s,"Учеба:%c%s",c2&0xF,profn[you.sprof]);
 if (you.spay<0)
 sprintf(s+i,"  %c%s\xFF  Ср.балл %c%.1f",studper(D)?c2&0xF:0x04,stper[studper(D)],c2&0xF,you.mark);
 prncc(y+9,x+2,s,c);
 y+=4;
 sprintf(s,"Время/сут.: Работа %c%.1fч.\xFF Учеба%c% .1fч.\xFF Своб. %c%.1fч.",c2&0xF,you.wtime/60.0,c2&0xF,sttime()/60.0,c2&0xF,(you.ftime-sttime())/60.0);
 prncc(y+6,x+2,s,c);
 i=sprintf(s,"ОC:%c%s (занимает %dM)",c2&0xF,OSnames[you.os],os[you.os].size>>10);
 if (you.osreq) sprintf(s+i," %cНадо %s%c",you.osreq==you.os?c2&0xF:0x04,OSnames[you.osreq],you.osreq==you.os?' ':'!');
 prncc(y+7,x+2,s,c);
 i=sprintf(s,"%luК \xFFКРУТОГО СОФТА%c",you.soft,c2&0xF);
 if (you.antiv.Date) sprintf(s+i," Антивирус от %d.%d.%d",
		     you.antiv.day(),you.antiv.month(),you.antiv.year()%100);
 prncc(y+8,x+2,s,c2);
 sprintf(s,"Месячный доход/расход %c$%d/~$%d\xFF  Долги %c$%ld",c2&0xF,you.income-(you.spay<0?you.spay:0),-you.expens+(you.spay>0?you.spay:0),c2&0xF,you.debt);
 prncc(y+9,x+2,s,c);
 sprintf(s,"Всего денег %c$%ld\xFF     Друзей: %c%d",c2&0xF,you.money,c2&0xF,you.friends);
 prncc(y+10,x+2,s,c);
 sprintf(s,"Настроение: %c%d%c хорошего %s\xFF   Усталость %c%d",c2&0xF,you.mood,'%',mood[you.mood/10],c2&0xF,you.tired);
 prncc(y+11,x+2,s,c);
 showtime();
 free(s);
}

void page(byte p)
{asm {
     mov al,p
     mov ah,5
     int 10h
 }
}

void final(char *st)
{char *s=salloc(1024);
 byte ar[80*24];
 sprintf(s,"%s%d %s. За это время вы потратили\nна почту %ld сут. %ld ч. %ld мин. чистого времени, получили %d плюс%s\nв конференциях, сменили %d модем%s и %d компьютер%s.",st,
	 D-SD,end(D-SD,end2),alltime/(24*60),alltime%(24*60)/60,alltime%(24*60)%60,
	 pluses,end(pluses),newm,end(newm),newc,end(newc));
 block(1,23,0xF);showstat(1,22,0x30);
 memcpy((byte far*)scrw+0x1000,scrw,4000);page(1);
 memset(ar,0,80*24);
 block(1,24,0x1F);
 message(s,0x1F,0);
 prnc(24,0,"                              Нажмите клавишу \"Anykey\"                         ",0x74);
 int i=80*24,j;
 while (i)
  if (!ar[j=random(80*24)]) {i--;ar[j]=1;scrw[j+0x800+80]=scrw[j+80];delay(20);}
 anykey();
 page(0);
 quit(0);
}

void getfdt(int f,word far *dt, word far *tm)
{asm {
 push ds
  mov bx,f
  mov ax,5700h
  int 21h
  lds bx,dt
  mov ds:[bx],dx
  lds bx,tm
  mov ds:[bx],cx
  pop ds
 }
}

void setfdt(int f, word dt, word tm)
{asm {
  mov bx,f
  mov cx,tm
  mov dx,dt
  mov ax,5701h
  int 21h
 }
}

struct memfile
{char *buff;
 byte *ptr;
 int f;
 word size,dt,tm;
 int open(char *name,word atr);
 int read(void *adr,word l);
 int write(void *adr,word l);
 int flush(byte closef=1);
};

int memfile::open(char *name,word atr)
{f=_open(name,atr);
 if (f==-1) return -1;
 size=lseek(f,0,2); // file length must be < 0xFFFF!
 if ((buff=(char*)malloc(size))==NULL) return -1;
 getfdt(f,&dt,&tm);
 lseek(f,0,0);
 _read(f,buff,size);
 ptr=(byte*)buff;
 return f;
}

int memfile::read(void *adr,word l)
{int noteof;
 if (ptr+l>(byte*)buff+size) {l=(byte*)buff+size-ptr; noteof=0;}
 else noteof=1;
 memmove(adr,ptr,l);ptr+=l;
 return noteof;
}

int memfile::write(void *adr,word l)
{int noteof;
 if (ptr+l>(byte*)buff+size) {l=(byte*)buff+size-ptr; noteof=0;}
 else noteof=1;
 memmove(ptr,adr,l);ptr+=l;
 return noteof;
}

int memfile::flush(byte closef)
{int fl;
 lseek(f,-(long)size,1);
 fl=_write(f,buff,size);
 setfdt(f,dt,tm);
 free(buff);
 return closef?close(f):fl;
}

memfile M;

int code(char *name)
{int i;
 if (M.open(name,0x4)==-1) return 0;
 char s[9];
 sprintf(s,"%04x%04x",M.tm^M.dt,~M.tm);
 for (i=0;i<M.size;i++)
  M.buff[i]^=s[i%8];
 return 1;
}

int save(char *fname)
{int f,i,zero=0;
 if ((f=_creat(fname,FA_ARCH))==-1) return 0;
 _write(f,&D.Date,sizeof(Date)*2);
 _write(f,&E,(dword)&you-(dword)&E);
 _write(f,&you.status,sizeof(you)-sizeof(char*));
 _write(f,&bbs,sizeof(bbs));
 for (i=0;i<E;i++)
 {_write(f,&(echoes[i]->stat),(dword)&(echoes[i]->izverg)-(dword)&(echoes[i]->stat)+sizeof(float));
  _write(f,echoes[i]->name,30);
  if (echodescr[i]!=NULL) _write(f,echodescr[i],30);
  else _write(f,&zero,30);
 }
 _write(f,you.name,30);
 for (i=0;i<4;i++) _write(f,&occup[i].ord,sizeof(occup[0].ord));
 if (you.sysop) _write(f,bbsnames[11],20);
 close(f);
 code(fname);
 M.flush();
 return 1;
}

int load()
{int f,i,j,e1=E;
 toccup tmpocp[4];
 if (!code("fido.dat")) return 0;
  char *s=salloc(30);
 M.read(&D.Date,sizeof(Date)*2);
 M.read(&E,(dword)&you-(dword)&E);
 M.read(&you.status,sizeof(you)-sizeof(char*));
 M.read(&bbs,sizeof(bbs));
 for (i=0;i<10;i++)
  bbs[i].name=bbsnames[i];
 for (i=LE+1;i<e1;i++) delete echoes[i];
 for (i=LE+1;i<E;i++) echoes[i]=new echo(i);
 for (i=0;i<E;i++)
 {M.read(&(echoes[i]->stat),(dword)&(echoes[i]->izverg)-(dword)&(echoes[i]->stat)+sizeof(float));
  M.read(s,30);
  if ((j=strlen(s))>strlen(echoes[i]->name))
   echoes[i]->name=(char *)realloc(echoes[i]->name,j+1);
  strcpy(echoes[i]->name,s);
  M.read(s,30);
  if (s[0]) strcpy(echodescr[i],s);
 }
 M.read(you.name,30);
 for (i=0;i<4;i++)
 {M.read(&tmpocp[i].ord,sizeof(occup[0].ord));
 tmpocp[i]=occup[tmpocp[i].ord-1];
 }
 memmove(&occup,&tmpocp,sizeof(occup));
 if (you.sysop) M.read(bbsnames[11],20);
 free(M.buff);
 close(M.f);
 free(s);
 return 1;
}

int yn(char *qst, int ans=0, char c1=0x70, char c2=0xF)
{int ls=0,k=0,i=0,s=1,n=1;
 while (qst[i]) if (qst[i++]=='\n') {if (k>ls) ls=k; k=0;n++;} else k++;
 if (k>ls) ls=k;
 int ll=max(ls+4,28);
 int t=10, l=(78-ll)>>1;
 void *q=openbox(t,l,t+5+n,l+ll,c1);
 write(t+2,l+2+(ls>24?0:24-ls)/2,qst);
 if (ans) s=ans;
con:
 prnc(t+3+n,l+2," А как же! ",s==1?c2:c1);
 prnc(t+3+n,l+ll-12," Вот еще!  ",s==1?c1:c2);
 if (ans) {delay(1000);goto ok;}
 switch (getch()) {
 case 13:goto ok;
 case 75:s==1?s=2:s--;break;
 case 77:s==2?s=1:s++;break;
 }
 goto con;
ok:
 closebox(t,l,t+5+n,l+ll,q);
 return (s==1);
}

void chmood(int dm)
{you.mood+=dm;
 if (you.mood<0)
 {block(1,24,0x4F);
  message("                      Это конец!\nВ приступе тяжелой депрессии вы  разбили молотком модем,\nвыкинули из окна компьютер и повесились на сетевом шнуре.\n                       RIP.",0x4F);
  quit(2);
 }
 if (you.mood<=10) message(" Депрессия до добра не доводит!\nНужно срочно поднять настроение!",0x4F);
 else if (you.mood>150) {if (you.mood-dm<150) message("Компьютер и модем - что еще человеку для счастья надо?",0x1F);
	  you.mood=150;}
}

void chrep(int dr,int chrp=1)
{int i;
 you.reput+=dr;
 if (you.reput>1024)
 {if (you.reput-dr<1024) message("И слух о вас гремит по всей Сети великой...",0x1F);
  you.reput=1024;
 }
 else if (dr<0)
  switch(you.status) {
  case 2: if (you.reput<128)
           if (chrp)
           {message("За особо раздражающее поведение вы лишены нодового адреса",0x4F);
  	    you.status=1;
	    maxpnt=you.points=0;
           }
           else you.reput=128;
          break;
  case 1: if (you.reput<32)
           if (chrp)
           {message("За плохое поведение босс погнал вас из поинтов",0x4F);
	    you.status=0;
	    for (i=0;i<=LE;i++) echoes[i]->stat=0;
            while (i<E) delecho(E-1);
           }
           else you.reput=32;
	  break;
  case 0: if (you.reput<-8)
           if (chrp)
	  {block(1,24,0x4F);
           message("Это ж кем надо быть, чтоб ни один сисоп не хотел иметь с вами дела!\n         Вообще таким, как вы, надо винт форматировать... \n                    Идите-ка отсюда, пока целы!",0x4F);
	   quit(1);
          }
          else you.reput=-8;
  }
}

long incsoft(long ds,int chrp=1)
{int d;
 if (you.soft+os[you.os].size+ds>you.hdspace) ds=you.hdspace-you.soft-os[you.os].size;
 if (!ds) return 0;
 chrep(random_(ds*you.status/512)/2,chrp);
 you.soft+=ds;
 return ds;
}

dword newday();

void OSinfo(int n)
{char *s=salloc(150);
 n--;
 sprintf(s,"Install time %2d min.\nSpace required %3dM",os[n].itime,os[n].size>>10);
 write(14,2,s);
 free(s);
}

int instOS(int n=0)
{int o,i,y=10,x=0,res=0;
 char *s=salloc(50);
 void *q;
 if (!n)
 {q=openbox(13,0,16,22,0x30);
  o=menuf(12,25,0x70,0x0F,OSnames,"Install",1,&OSinfo);
  closebox(13,0,16,22,q);
 } else o=n+1;
 if (o)
 {o--;
  if (os[o].itime>Time) {message("Сегодня не успеем...",0x4F);goto all;}
  if (os[o].mincomp>you.comp)
  {message("У вас слишком хилый компьютер!",0x4F);goto all;}
  if (you.soft+os[o].size>you.hdspace)
  {message("Не хватает места на винте!",0x4F);goto all;}
  q=openbox(y,x,y+6,x+40,0x0F);
  sprintf(s,"Installing %s...",OSnames[o]);
  prn(y+1,x+1,s);
  for (i=1;i<=os[o].itime;i++)
  {sprintf(s,"%d%% complete",i==os[o].itime?100:i*100/os[o].itime);
   prn(y+3,x+2,s);
   Time--;showtime();
   if (o>0 && _rnd(400/(you.skill[1]+1)) && !_rnd(10))
   {message("Глюки!!! Придется переинсталлировать заново...",0x4F);goto all;}
   delay(400);
  }
  closebox(y,x,y+6,x+40,q);
  you.os=o;res=1;
  if (you.osreq) you.wdate=D+6;
 }
all:
 free(s);
 return res;
}

void fire()
{chrep(-random(10)-5);
 if ((you.skill[you.wprof]-=15)<0) you.skill[you.wprof]=0;
 chmood(-15-_rnd((you.income)/(you.wtime/60.0)/8));
 you.ftime+=you.wtime;you.wtime=0;you.wdays=0;
 you.income=0;you.wprof=0;you.osreq=0;
}

void expel()
{if ((you.skill[you.sprof]-=10)<0) you.skill[you.sprof]=0;
 chmood(-10-random(8));
 you.spay=0;you.sdays=0;you.grad=0;you.sprof=0;
 if (you.army==1) you.army=3;
}

void newjob(int pay,int time,int prof)
{if (you.wdays>7) you.money+=you.income*(float)(you.wdays%30)/30;
 you.ftime+=you.wtime;you.wtime=time;you.ftime-=you.wtime;you.wprof=prof;
 you.income=pay;you.wdays=0;
 you.osreq=0;you.wdate=0;
}

#define newinfo(i) (echoes[(i)]->read>random(100))

int joffer(int wait=1)
{char *s=salloc(50*6);
 void *q;
 if (newinfo(6))
 {char *var[6];
  int vars[6][3];	//з/п, время, профиль
  int n,k,j;
  if (wait) {newdayf=1;if (tstbit(newday(),14)) goto all;}
  if (max(you.skill[1],you.skill[3])>=4096 && !random(5))
  {if (you.skill[1]>you.skill[3] || (you.skill[1]>4096 && you.money<1000L))
   {message("        Специальное предложение!      \nВы можете получить постоянную работу в США.\n  Начальная зарплата - $5000 в месяц. ",0x1F);
    if (yn("Согласны?"))
    {final("Ваш программистский уровень был оценен по достоинству. Вы уехали в Штаты.\nПередавайте привет Пажитнову и остальным нашим! Теперь вам не до ФИДО...\n \nВаша фидошная карьера продолжалась ");}
   }
   else if (you.money>1000L)
   {message("             Специальное предложение!          \nВы можете открыть свою собственную торговую фирму.",0x1F);
    if (yn("Согласны?"))
    {final("Ну вот вы и новый русский. Или не русский? Впрочем, какая разница...\n    Теперь вам не до ФИДО. Ваша дальнейшая биография может быть\n       не менее интересной, но это уже совсем другая история...\n \nВаша фидошная карьера продолжалась ");}
   }

  }
  q=openbox(10,11,12,45,0x70);
  echoes[6]->read=0;
  sprintf(s,"Предложения работы в %s",echoes[6]->name);
  prn(11,12+strlen(pref)/2,s);
  n=random(6)+1;
  for (k=0;k<n;k++)
  {vars[k][2]=random(3)+1;
   vars[k][1]=2*60+random(Stable?12:20)*30;
   vars[k][0]=vars[k][1]/60.0*(30+random_(you.skill[vars[k][2]]-64)/64.0*5+(you.comp-3)*5);
   sprintf(s+50*k,"%-20s  $%-4d        %.1f ч.",profn[vars[k][2]],vars[k][0],vars[k][1]/60.0);
   var[k]=s+50*k;
  }
  var[n]=NULL;
  j=menu(13,14,0x70,0x0F,var," Профиль              З/п в месяц  Время в день",1);
  closebox(10,11,12,45,q);
  if (j--)
  {Down=1;newdayf=1;newday();
   if (you.income+random(80)+you.skill[vars[j][2]]/8+random_(you.skill[vars[j][2]]/4)+_rnd(you.comp*10)<vars[j][0])
   {message("Вы не прошли собеседование",0x4F);goto no;}
   newjob(vars[j][0],vars[j][1],vars[j][2]);
all:free(s);
   return 1;
  }
 }
 else
 {sprintf(s,"Читайте эху %s",echoes[6]->name);message(s,0x4F);}
 no:free(s);
 return 0;
}

void fidomess(char *from,char* to,char *subj,char *text,int y=5,int x=8)
{void *q=openbox(y,x,y+16,x+60,0x1E);
 int i;
 prnc(y+1,x+1,"From : ",0x13);prnc(y+1,x+8,from,0x13);
 prnc(y+2,x+1,"To   : ",0x13);prnc(y+2,x+8,to,strcmp(to,you.name)?0x13:0x1F);
 prnc(y+3,x+1,"Subj : ",0x13);prnc(y+3,x+8,subj,0x13);
 for (i=(x+1);i<(x+60);i++) scrs(y+4,i,'─');
 scrs(y+4,i,195);scrs(y+4,60+x,180);
 prn(y+5,x+1,"Hi ");i=wrtword(y+5,x+4,to);scrs(y+5,x+4+i,'!');
 i=write(y+7,x+1,text);
 wrtword(y+8+i,x+1,from);
 anykey();
 closebox(y,x,y+16,x+60,q);
}

int proposal(int i)
{char *from[]={"Don Carleone","Vasya Pupkin","Sergey Mavrodi"};
 int d,summ,pay=0;
 char *s=salloc(2048);
 switch(i) {
 case 1:sprintf(s,"Есть деловое предложение для крутого хакера.\nНадо взломать кой-какую защиту. Плачу $%d.",summ=random(you.skill[1]*5)+100);
	d=random(5)+2;break;
 case 2:sprintf(s,"Я слышал, вы можете компьютер наладить. За $%d возьметесь?",summ=random(4)*10+20);
	d=1;break;
 case 3:pay=random(you.skill[3])*5+50;
	sprintf(s,"Предлагаю выгодный совместный бизнес.\nВложив всего $%d, вы получите $%d!",pay,summ=pay*(2+random(4)));
	d=random(4)+2;break;
 }
 fidomess(from[i-1],you.name,"Предложение",s);
 if (!yn("Вы принимаете предложение?")) return 0;
 Down+=d;you.money-=pay;
 sprintf(s,"Напряженный труд занял %d %s...",d,end(d,end2));
 message(s,0x71);
 newdayf=1;
 while (d) {newday();d--;}
 switch(i) {
 case 1:if (random(summ)>you.skill[1]*2)
	{message("Ничего не вышло. Защита оказалась слишком сложной для вас.\nЭто не пойдет на пользу вашей профессиональной репутации.",0x4F);
	 you.skill[1]-=random(5);break;
	}
	else if (!_rnd(you.skill[1]>>7))
	{sprintf(s,"У вас крупные неприятности. Те, чью защиту вы ломали, пожелали\nузнать, кто это такой умный, и им это удалось. Придется вам\nзаплатить им $%d, и считайте, что дешево отделались!\n",summ*=2);
         summ=-summ;you.skill[1]-=random(10);
	 message(s,0x4F);
        }
	else {you.skill[1]+=random(5);message("Нет такой защиты, которую нельзя было бы сломать!",0x1F);}
	you.money+=summ;
	break;
 case 2:if (!_rnd(you.skill[2]>>7))
	{message("Вам не удалось совладать с железом заказчика\nЭто не пойдет на пользу вашей профессиональной репутации.",0x4F);
	 you.skill[2]-=random(5);}
	else {you.skill[2]+=random(5);message("Не так страшно кривое железо, как кривые руки...\nК счастью, вы этим не страдаете!",0x1F);
	you.money+=summ;}
	break;
 case 3:if (random(pay)>you.skill[3]*2)
	{message("Плакали ваши денежки...",0x4F);
	 you.skill[3]-=random(5);break;
	}
	else if (!_rnd(you.skill[3]>>7))
	{sprintf(s,"Пора бы знать, что честный бизнес таких прибылей не приносит.\nТе, кого вы пытались кинуть, оказались не лохами, и теперь \nвам придется заплатить им $%d!\n",summ);
	message(s,0x4F);summ=-summ;you.skill[3]-=random(10);}
	else {you.skill[3]+=random(5);message("Дело было рискованным, но риск себя оправдал.",0x1F);}
	you.money+=summ;
	break;
 }
 free(s);
 return 1;
}

int echo::moderatorial(int y,int x)
{char *nn[]={" "," второй "," третий "};
 int i,d;
 if (random(100)<prob[Style]*izverg*(1+(float)_rnd(you.points)/32))
 {char *s=salloc(160);
  i=sprintf(s,"За нарушение правил вы получили%sПЛЮС", nn[plus]);
  plus++;pluses++;d=-2;
  if (plus==3)
   {stat=0;dl=D+92;
    sprintf(s+i,"\nи отключены от конференции до %d.%d.%d",dl.day(),dl.month(),dl.year());
    d-=5;
   }
  char *from=salloc(50);
  sprintf(from,"Moderator of %s",name);
  fidomess(from,you.name,plus>2?"moderatorial [!]":"moderatorial [+]",s,y,x);
  free(from);
  free(s);
  chrep(d);
  chmood(-(2<<plus));
  return 1;
 }
 return 0;
}

int netmail::event()
{int i;
 traf+=_rnd(Style*3)-2;
 if (traf<0) traf=0;
 traf*=Style/float(1.5+_rnd(Style*2)/4.0);
 while ((dword)echtime(0)>24*60) traf/=2;
 chmood(_rnd(traf) >> 2);
 if (Style==3) {if ((you.friends-=!random(20))<0) you.friends=0;}
 else you.friends+=(random(Style+1) && !random(16));
 for (i=1;i<4;i++)
  if (_rnd(you.skill[i]>>6) && !random(10))
   if (proposal(i)) break;
 return traf;
}

int local::event()
{traf+=_rnd(Style*2)+_rnd(5)-2;
 if (you.status>1)
  if (Style==3 || !Style) traf*=(5.0-Style+random(5))/10;
 if (traf<0) traf=0;
 while ((dword)echtime(0)>24*60) traf/=2;
 chmood(_rnd(traf) >> 3);
 return traf;
}

int point::event()
{register int d;
 if (you.points<maxpnt && !random(3))
 {d=you.points;
  you.points+=random(4);
  if (you.points>=maxpnt) {you.points=maxpnt;maxpnt=0;}
  chrep((you.points-d)*(4+random(2)));
  if (d) echoes[1]->traf*=(float)you.points/d;
  else echoes[1]->traf+=random(5)*you.points;
  return 1;
 }
 return 0;
}

int ruanekdot::event()
{int i=random(3);
 chmood(i);
 return i;
}

int job::event()
{if (random(20) || BBSf) return 0;
// joffer(0);
 return 1;
}

int vcool::event()
{int k;
 if (random(20) || you.reput<0) return 0;
 char *s=salloc(80);
 switch (random(5))
 {case 0:if (!you.wprof) break;
         k=(_rnd(you.reput>>2)/10)*10;if (!k) k=5;
	 you.income+=k;
	 sprintf(s,"Информация из эхи VERY.COOL позволила вам зарабатывать на $%d больше!",k);
	 message(s,0x1F);
	 break;
  case 1:if (you.ftime<5*60)
	  if ((k=(random(3)+1)*10)<you.wtime-60)
	  {you.ftime+=k;you.wtime-=k;
	   sprintf(s,"Информация из эхи VERY.COOL позволила вам освободить %d минут в день!",k);
	   message(s,0x1F);
	  }
	 break;
  default:
	 k=_rnd(you.reput_()>>3)+1;
	 you.money+=k;
	 sprintf(s,"Информация из эхи VERY.COOL позволила вам заработать $%d!",k);
	 message(s,0x1F);
 }
 free(s);
 return 1;
}

int fecho::event()
{int l;
 if (random(5)) return 0;
 l=random(1024)+32;
 l=incsoft(l);
 you.virus+=random(l)<(l>>5);
 if (!random(5))
 {you.antiv=D;
  message("По файлэхе пришел свежий антивирус! Полезная вещь...",0x1F);
  chmood(1);
 }
 return 1;
}

int exch::event()
{if (!random(8)) you.skill[3]++;
}

int bllog::event()
{if (!random(8)) you.skill[3]++;
}

int hardw::event()
{if (!random(3)) you.skill[2]++;
}

int softw::event()
{if (!random(3)) you.skill[1]++;
}

int test(question tst[],int N,int y,int x)
{int j,k;
 char c;
 char *s=salloc(50);
 do j=random(N); while (tst[j].mark);
 tst[j].mark=1;
 clrbl(y+1,x+2,y+6,x+49,0x0F);
 write(y+1,x+2,tst[j].qstn);
 for(k=0;k<3;k++)
 {sprintf(s,"%d) %s",k+1,tst[j].ans[k]);prn(y+4+k,x+3,s);}
 free(s);
 do ; while (!((c=getch())>'0' && c<'4'));
 c-=0x31;
 return (tst[j].correct==c);
}

void BBSinfo(int n)
{int y=14,x=0,i;
 n--;
 char *s=salloc(150);
 box(y,x,y+5,x+19,0x30);
 i=sprintf(s,"Модем на %u\nUploaded %lu\nDownloaded %lu\n",bps[bbs[n].modem],bbs[n].U,bbs[n].D);
 if (bbs[n].down) sprintf(s+i,"       DOWN       ");
 else if (bbs[n].mxtime==-1) sprintf(s+i,"       TWIT       ");
 else if (bbs[n].mxtime) sprintf(s+i,"Time left %3d min",bbs[n].time);
 write(y+1,x+1,s);
 free(s);
}

int session(int *k1,int cps,word con,int y,int x,char *s)
{int i,j,p=100,bad=0;
  for (i=1;i<=*k1 && Time;i++)
  {j=sprintf(s,"%d%%  %d cps    ",p=i*100/(*k1),int(cps*(.9+_rnd(21)/100.0)));
   prnc(y,x,s,0x07);
   Time--;showtime();
   cps>>=bad;i-=bad;
   if (cps<=con/100) {prn(y,x+j+2,"Cancelled");delay(1500);break;}
   if (!_rnd(50+you.modem*10)) bad=1;
   delay(400);
  }
  *k1=i-1;
  return p;
}

int loadfile(char *name,char *where)
{int f;
 if ((f=_open(name,1))==-1) return 0;
 int size=lseek(f,0,2); // file length must be < 0xFFFF!
 lseek(f,0,0);
 size=_read(f,where,size);
 close(f);
 return size;
}

void callBBS(int n) //n - BBS number
{void *q;
#define PicSize 16*50*2
 char c,*s=salloc(60),*title=salloc(PicSize);
 int i,j,p,k1,k=random(50);
 word con,cps,t0=Time;
 long u,u1;
 LastBBS=n;
 q=openbox(6,18,23,70,0x0F);
 if (bbs[n].down)
 {prn(8,22,"BBS temporary down... Sorry");
  goto all;
 }
 prn(22,21,"Dialing... Press <ESC> to abort");
 for (;k;k--,Time--)
 {if (!Time) goto all1;
  prn(7,22,"BUSY");
  delay(200);
  if (ESC) goto all;
  prn(7,22,"    ");
  delay(200);
  showtime();
 }
 prn(22,21,"                               ");
 con=min(bps[you.modem],bps[bbs[n].modem]);
 sprintf(s,"CONNECT %u",con);
 prn(7,22,s);
 prn(8,22,"Press <ESC>-<ESC> to enter BBS");
 while (getch()!=27);
 while (getch()!=27);
 clrbl(7,19,22,69,0x0F);
 sprintf(s,"%d.Bin",n+1);
 if (i=loadfile(s,title))
 {if (i>PicSize) message("Недопустимый размер картинки! Срочно выходите в ДОС!",0xCF);
  title[i]=0;
//  write(7,19,title);
  for (j=0;j<16;j++)
   memmove(&scr[(7+j)*160+19*2],&title[j*50*2],50*2);
  anykey();
 }
 clrbl(7,19,22,69,0x0F);
 if (bbs[n].mxtime==-1)
 {prn(7,22,"Пошел ВОН!!!");
  delay(3000);
  goto all;
 }
 else if (!bbs[n].mxtime)
 {prn(7,22,"Sysop рад приветствовать нового юзера!");
  bbs[n].time=bbs[n].mxtime=20+_rnd(5)*5;
 }
 k=min(Time,bbs[n].time);
 BBSf=1;
 nxt:
 sprintf(s,"У вас %d мин.                   ",k);
 prn(22,21,s);
 showtime();
 if (!k) goto all;
 prn(9,22,"F - File areas  M - Message areas  G - GoodBye");
 cps=con/(10+random(10));
 c=getch();
 clrbl(7,19,22,69,0x0F);
 switch (upcase(c)) {
  case 'F':prn(9,22,"File areas                                     ");
	   prn(11,23, "U-Upload to us  D-Download to you");
	   c=getch();
           prn(11,23, "                                 ");
	   switch(upcase(c)) {
	   case 'U':u=min(((long)cps*k*60)>>10,u1=you.soft-bbs[n].D-bbs[n].U);
		    if (u<=0)
		    {prn(13,23,"   0K send                             ");
		     goto nxt;
		    }
		    if (u==u1) k1=(u<<10)/((dword)cps*60);else k1=k;
		    if ((p=session(&k1,cps,con,13,23,s))==100) k-=k1;
		    else {k=0;u*=p/100.0;}
		    bbs[n].time-=k1;
		    bbs[n].U+=u;
		    sprintf(s,"   %luK send, CPS %d                   ",u,cps);
		    prnc(13,23,s,0x0F);
		    if (random(you.virus+1))
		    {bbs[n].mxtime=-1;
		     message("Вы закачали на BBS вирус, и сисоп поставил вам twit!\n     Теперь даже и не пытайтесь звонить сюда!",0x4F);
		     chmood(-(9-(you.status<<1)));
		     chrep(-5);
		     goto all;
		    }
		    chrep(u>>(9+(you.reput>>5)));
		    break;
	   case 'D':u=min(((dword)cps*k*60)>>10,bbs[n].soft);
		    u=min(u,you.hdspace-you.soft-os[you.os].size);
		    if (u==bbs[n].soft || u==you.hdspace-you.soft-os[you.os].size)
		     k1=(u<<10)/((dword)cps*60);
		    else k1=k;
		    if ((p=session(&k1,cps,con,13,23,s))==100) k-=k1;
		    else {k=0;u*=p/100.0;}
		    bbs[n].time-=k1;
		    bbs[n].soft-=u;bbs[n].D+=u;u=incsoft(u);
		    i=sprintf(s,"   %luK received",u);
		    if (u) sprintf(s+i,", CPS %d          ",cps);
		    prnc(13,23,s,0x0F);
		    if (!u) break;
		    chmood(u>>11);
		    if (!random(10))
		    {you.antiv=D;
		     message("Вы скачали свежий антивирус! Полезная вещь...",0x1F);
		     chmood(1);
		    }
		    you.virus+=((lrandom(u)<(u>>5)));
		    break;
	   case 27: clrbl(7,19,22,69,0x0F);
		   goto nxt;
	   }
	   bbs[n].mxtime+=5*random_(bbs[n].U-(bbs[n].D>>2) >> 8);
	   if (bbs[n].mxtime<5) bbs[n].mxtime=5;
	   else if (bbs[n].mxtime>180) bbs[n].mxtime=180;
	   goto nxt;
  case 'M':prn(9,22,"Message areas                                ");
	for (i=2,j=1;i<LE;i++)
	    if (bbs[n].ech[i-2])
	     {sprintf(s,"%d) %s",i-1,echoes[i]->name);prn(10+j++,22,s);}
	   getc:c=getch();
	   if (c>'0' && c<'9' && bbs[n].ech[c-'0'-1])
	   {c-=0x30-1;
	    if (!echoes[c]->stat)
	    {if (k<(j=echoes[c]->traf*echoes[c]->trafk))
	     {echoes[c]->read=k/j*100.0;k1=k;}
	     else {k1=j;echoes[c]->read=100;}
	     k-=k1;Time-=k1;bbs[n].time-=k1;
	     if (random(100)<echoes[c]->read) echoes[c]->event();
	    }
//	    clrbl(15,21,22,69,0x0F);
//            goto nxt;
	   }
	   else if (c!=27) goto getc;
	   clrbl(7,19,22,69,0x0F);
	   break;
  case 'G':clrbl(7,19,22,69,0x0F);goto all;
 }
 goto nxt;
all:
 prn(22,21," NO CARRIER                     ");
 anykey();
all1:
 BBSf=0;
 alltime+=t0-Time;
 closebox(6,18,23,70,q);
 showstat(1,22,0x30);
 free(s);free(title);
}

void setpref(char **list)
{int i;
 char *s; //memory will be allocated for strings
 for (i=0;list[i]!=NULL;i++) if (list[i][0]=='*')
 {s=salloc(strlen(pref)+strlen(list[i]));
  strcpy(s,pref);strcat(s,list[i]+1);list[i]=s;
 }
}

int vircheck(int y,int x)
{void *q;
 long i,t;
 if (!you.antiv.date) {message("Дык нету у вас антивируса!",0x4F);return 0;}
 t=you.soft/(1024+you.comp*2048);
 if (t>=Time) {message("Сегодня не успеем провериться...",0x4F);return 0;}
 q=openbox(y,x,y+6,x+40,0x0F);
 prn(y+1,x+1,"Antivirus starts...");
 char *s=salloc(15);
 for (i=0;i<=t;i++)
 {sprintf(s,"%lu%% complete",i==t?100:i*100/t);
  prn(y+3,x+2,s);
  Time--;showtime();
  delay(400);
 }
 lstscn=D;
 i=you.virus/(_rnd((D-you.antiv)>>3)+1);
 if (i)
 {sprintf(s,"%d virus(es) found & cured!",i);you.virus-=i;
  prnc(y+4,x+1,s,0x0C);
 } else prn(y+4,x+1,"No viruses found");
 if (D-you.antiv>16) prn(y+5,x+1,"Warning: you antivirus is too old!");
 anykey();
 closebox(y,x,y+6,x+40,q);
 free(s);
 return i;
}

int wear(int *reli)
{*reli*=0.9992;
 int i=rand();
 return (i>(*reli) && !_rnd(4+(echoes[8]->read?4:0)+(you.skill[2]>>4)));
}

int decmoney(int x)
{if ((you.money-=x)<0)
 {message("Вы залезли в долги! Это может плохо кончиться!",0x4F);
  return 1;}
 else return 0;
}

int chktrf(int traf)
{if ((traf)*1024L/(bps[you.modem]/10)/60>30)
 {message("У вас слишком медленный модем для такого трафика",0x4F);return 0;}
 return 1;
}

int echlink(int echn=0,int y=4,int x=10)
{void *q;
 int i,j,traf=0,sel;
 char c;
 if (echn) {sel=echn; if (echoes[sel]->stat) return 1;}
 else sel=2;
 q=openbox(y,x,y+18,x+40,0x1E);
 prnc(y+1,x+1,"From : ",0x13);prnc(y+1,x+8,you.name,0x1F);
 prnc(y+2,x+1,"To   : AreaFix",0x13);
 for (i=(x+1);i<(x+40);i++) scrs(y+3,i,'─');
 scrs(y+3,x,195);scrs(y+3,40+x,180);
 for (i=2;i<E;i++)
 {prn(y+2+i,x+2,echoes[i]->name);
  if (echoes[i]->stat)
  {scrs(y+2+i,x+1,'+');
   traf+=echoes[i]->traf;
  }
 }
 select:
  for(i=x+2;i<x+30;i++) scra(y+2+sel,i,0x0F);
 if (echn) goto marking;
 do c=getch();while (!c);
 switch (c) {
  case 27:c=0;goto all;
  case 13:selected:c=1;
	  all:if (!chktrf(traf)) {echn=0;goto select;}
          if (echn && !echoes[echn]->stat) c=0;
	  for (i=LE+1;i<E;)
	   if (!echoes[i]->stat)
	   {delecho(i);chrep(-4-random(3));
	   }
	   else i++;
	  closebox(y,x,y+18,x+40,q);return c;
  case 32:
  if (echoes[sel]->stat)
	  {echoes[sel]->stat=0;traf-=echoes[sel]->traf;
	   scrs(y+2+sel,x+1,'-');
	   if (sel>LE) message("Учтите - ваша эха без вас не выживет!",0x4F);
	  }
	  else
          marking:
          if (echoes[sel]->plus<3)
	  {if (chktrf(traf+echoes[sel]->traf))
	   {traf+=echoes[sel]->traf;echoes[sel]->stat=sel<=LE?1:2;
	    scrs(y+2+sel,x+1,'+');
	    echoes[sel]->dl=D;
	    echoes[sel]->msg=echoes[sel]->newm=echoes[sel]->new1=0;
	   }
	  }
          if (echn) goto selected;
	  break;
  case 73:/*PgUp*/
	if (sel>2) {for(i=x+2;i<x+30;i++) scra(y+2+sel,i,0x1E);sel=2;}
	break;
  case 81:/*PgDn*/;
	if (sel<E-1) {for(i=x+2;i<x+30;i++) scra(y+2+sel,i,0x1E);sel=E-1;}
	break;
  case 72:for(i=x+2;i<x+30;i++) scra(y+2+sel,i,0x1E);
	sel==2?sel=E-1:sel--;break;
  case 80:for(i=x+2;i<x+30;i++) scra(y+2+sel,i,0x1E);
	sel==E-1?sel=2:sel++;break;
  }
  goto select;
}

void readres(int k)
{switch (Style) {
  case 3:chrep((random(5)-3)*k);chmood(random(6)-1);break; //flame
  case 2:chrep(random(k+you.moder*2));chmood(_rnd(k>>1));break;
  case 1:if (k) {chrep(random(you.moder+2));chmood(_rnd(2));} break;
 }
}

dword echread(int au=1,int y=6,int x=2)
{void *q=openbox(y,x,y+LE+7,x+74,0x1B);
 char *s=salloc(80);
 char c;
 char marks[]={' ','√','p'};
 int i,j,k,l,t,lost,lim,sel,traf=0;
 int autor;
 float rd;
 dword res;
 int area[LE+6];
 prncc(24,0," \x04Space\xFF\ Autoread │ \x04P\xFF\x61ssthru │\x04 Enter\xFF\ Read echo │ \x04-> \xFFRead 1 message │\x04 Esc\xFF\ Exit    ",0x70);
 prnc(y,x+3,"Description",0x1E);
 prnc(y,x+38,"Msgs",0x1E);
 prnc(y,x+43,"New",0x1E);
 prnc(y,x+48,"EchoID",0x1E);
 for (i=k=0;i<E;i++)
  if (echoes[i]->stat && echodescr[i]!=NULL)
  {sprintf(s,"%c%-35s│%4d│%4d│%-25s",
	   marks[echoes[i]->mark],echodescr[i],echoes[i]->msg,echoes[i]->newm,echoes[i]->name);
   prn(y+1+k,x+1,s);
   area[k]=i;
   k++;
  }
 l=k;
 for(;k<LE+6;k++)
 {scrs(y+1+k,x+37,'│');scrs(y+1+k,x+42,'│');
  scrs(y+1+k,x+47,'│');
 }
 scrs(y+LE+7,x+37,193);scrs(y+LE+7,x+42,193);
 scrs(y+LE+7,x+47,193);
 scrs(y,x+37,194);scrs(y,x+42,194);
 scrs(y,x+47,194);
 if (echoes[10]->stat)
 {autor=2;
  sel=l;area[sel]=10;
  goto rd1;
 }
 rd4:
 autor=1;
 for (sel=0;sel<l;sel++)
 {if (echoes[area[sel]]->mark & 1) goto rd1;
  rd0:if (Time<2) break;
 }
 if (!au)
 {for (sel=0;sel<l;sel++)
   if (echoes[area[sel]]->newm && echoes[area[sel]]->mark<2) goto rd5;
  goto all;
 }
 rd5:
 autor=sel=0;
 select:
  for(i=x+2;i<x+73;i++) scra(y+1+sel,i,0x0F);
 c=getch();
 switch (upcase(c)) {
  case 27:goto all;
  case 13:
  rd1:if (echoes[area[sel]]->mark & 2) goto rd3;
    Time-=(t=echtime1(area[sel],echoes[area[sel]]->newm));
    if (!t) goto rd3;
    rd=1.0;
    if (Time<=0) {rd=(t+Time-1.0)/t;Time=1;alltime+=Time-1;} else alltime+=t;
    if (!(j=echoes[area[sel]]->newm*rd)) goto rd3;
mesread:
    echoes[area[sel]]->newm-=j;
    if ((echoes[area[sel]]->read+=100.0*j/echoes[area[sel]]->new1)>100)
     echoes[area[sel]]->read=100;
    showtime();
    if (autor<2)
    {sprintf(s,"%4d",echoes[area[sel]]->newm);
     prn(y+1+sel,x+43,s);
     if (area[sel]>1) echoes[area[sel]]->traf+=int(_rnd(Style*2)+_rnd(5)-2)*rd;
     traf+=j;
    }
    if (random(100)<rd*100 && echoes[area[sel]]->event()) setbit(res,area[sel]+8);
    if (echoes[area[sel]]->stat==2)
    {if (Style==3 || !Style) echoes[area[sel]]->traf*=(5.0-Style+random(5))/10;
    }
    if (newdayf) {newdayf=0;goto all;}
    rd3:switch (autor)
    {case 1:goto rd0;
     case 2:goto rd4;
    }
  break;
  case 32:
	    echoes[area[sel]]->mark&=1;
	    echoes[area[sel]]->mark^=1;
            goto chmark;
  case 'P': if (area[sel]>LE) break;
	    echoes[area[sel]]->mark&=2;
	    echoes[area[sel]]->mark^=2;
     chmark:scrs(y+1+sel,x+1,marks[echoes[area[sel]]->mark]);
	  break;
  case 0:switch (c=getch()) {
   case 77:/*right*/
          if (echoes[area[sel]]->mark & 2) break;
	  if (echoes[area[sel]]->newm) t=echtime1(area[sel],1); else break;
	  if (t>=Time) {t=0;break;}
	  Time-=t;alltime+=t;
	  j=1;rd=1.0/echoes[area[sel]]->new1;
	  goto mesread;
   case 73:/*PgUp*/
	 if (sel>0) {for(i=x+2;i<x+73;i++) scra(y+1+sel,i,0x1B);sel=0;}
	 break;
   case 81:/*PgDn*/;
	 if (sel<l-1) {for(i=x+2;i<x+73;i++) scra(y+1+sel,i,0x1B);sel=l-1;}
	 break;
   case 72:for(i=x+2;i<x+73;i++) scra(y+1+sel,i,0x1B);
	 sel==0?sel=l-1:sel--;break;
   case 80:for(i=x+2;i<x+73;i++) scra(y+1+sel,i,0x1B);
	 sel==l-1?sel=0:sel++;break;
   }
  }
  goto select;
 all:
 if (traf)
 {k=traf/40 %20;
  readres(k);
 }
 free(s);
 closebox(y,x,y+LE+7,x+74,q);
 showhelp();
 return res;
}

void buycomp(int wait=0)
{char *ar[8],*var[6];
 int vars[5][2];	//цена, надежность
 char *warn="Не можете же вы жить совсем без компьютера!";
 char *s=salloc(12*5);
 void *q;
 int i=0,n,k,j,cpr;
 if (!wait)
 {j=random(2)+2;
  sprintf(s,"На поиск предложений ушли %d %s...",j,end(j,end2));
  message(s,0x71);
 } else j=wait;
 for (;j;j--) if (tstbit(newday(),1)) goto all;
 cpr=you.comp==0xFF?0:cprice[you.comp]*0.9;
 do ar[i]=comp[i++];
 while (cprice[i]<=you.money && i<7);
 ar[i]=NULL;
 q=malloc(22*10*2);
 gettext(4,11,25,20,q);
 sel:i=menuncl(10,3,0x2F,0x0F,ar,"Компьютеры",1);
 if (i)
 {i--;
  n=1+random(echoes[3]->read/25+1);
  for (k=0;k<n;k++)
  {vars[k][1]=24576+random(8192);
   vars[k][0]=cprice[i]*(you.skill[3]>640?0.8:(1.2-you.skill[3]/1600.0))*vars[k][1]/(24576+random(8192));
   sprintf(s+12*k,"$%-4d  ",vars[k][0]);
   if (echoes[4]->read) sprintf(s+12*k+6,"  %2d%%",(dword)vars[k][1]*100/32768);
   var[k]=s+12*k;
  }
  var[n]=NULL;
  sel1:
  j=menu(10,14,0x70,0x0F,var,echoes[4]->read?" Цена  Надежн.":"Цена",1);
  if (!j && you.comp==0xFF)
  {message(warn,0x4F);goto sel1;}
  if (j)
  {decmoney(vars[--j][0]-cpr);
   if (you.comp!=0xFF) chmood((i-you.comp)*(random(3)+1));
   you.comp=i;you.creli=vars[j][1];
   if (os[you.os].mincomp>you.comp) {you.os=0;
    if (you.osreq) you.wdate=D+6;
   }
   newc++;
   if (cpr)
   {sprintf(s,"Ваш старый компьютер продан за $%d",cpr);
    message(s,0x71);
   }
  }
 }
 else if (you.comp==0xFF)
      {message(warn,0x4F);goto sel;}
 puttext(4,11,25,20,q);free(q);
all:free(s);
}

void buymodem(int wait=0)
{char *ar[7],*var[6];
 int vars[5][2];	//цена, надежность
 char *warn="Вы должны купить хоть какой-нибудь модем!";
 char *s=salloc(70+12*5);
 void *q;
 int i=0,n,k,j,mpr,traf=0;
 if (!wait)
 {j=random(2)+2;
  sprintf(s,"На поиск предложений ушли %d %s...",j,end(j,end2));
  message(s,0x71);
 } else j=wait;
 for (;j;j--) if (tstbit(newday(),0)) goto all;
 mpr=you.modem==0xFF?0:mprice[you.modem]*0.9;
 do ar[i++]=ultoa(bps[i],s+i*10,10);
 while (mprice[i]<=you.money && i<6);
 ar[i]=NULL;
 q=malloc(14*14*2);
 gettext(4,11,15,24,q);
 sel:i=menuncl(10,3,0x2F,0x0F,ar,"Модемы",1);
 if (i)
 {i--;
  n=1+random(echoes[3]->read/25+1);
  for (k=0;k<n;k++)
  {vars[k][1]=24576+random(8192);
   vars[k][0]=mprice[i]*(you.skill[3]>640?0.8:(1.2-you.skill[3]/1600.0))*vars[k][1]/(24576+random(8192));
   sprintf(s+70+12*k,"$%-4d  ",vars[k][0]);
   if (echoes[4]->read) sprintf(s+70+12*k+6,"  %2d%%",(dword)vars[k][1]*100/32768);
   var[k]=s+70+12*k;
  }
  var[n]=NULL;
  sel1:
  j=menu(10,14,0x70,0x0F,var,echoes[4]->read?" Цена  Надежн.":"Цена",1);
  if (!j && you.modem==0xFF)
  {message(warn,0x4F);goto sel1;}
  if (j)
  {decmoney(vars[--j][0]-mpr);
   if (you.modem!=0xFF) chmood((i-you.modem)*(random(3)+1));
   if (mpr)
   {sprintf(s,"Ваш старый модем продан за $%d",mpr);
    message(s,0x71);
   }
   you.modem=i;you.mreli=vars[j][1];
   newm++;
  }
 }
 else if (you.modem==0xFF)
      {message(warn,0x4F);goto sel;}
 puttext(4,11,15,24,q);free(q);
all:free(s);
 if (you.status)
 {for (i=2;i<E;i++)
   if (echoes[i]->stat) traf+=echoes[i]->traf;
  if (!chktrf(traf)) echlink();
 }
}

void buyhd(int wait=0)
{char *ar[8],*var[6];
 int vars[5][2];	//цена, надежность
 char *s=salloc(70+12*5);
 void *q;
 int i=0,n,k,j,hpr;
 if (!wait)
 {j=random(2)+2;
  sprintf(s,"На поиск предложений ушли %d %s...",j,end(j,end2));
  message(s,0x71);
 } else j=wait;
 for (;j;j--) newday(); // if (tstbit(,0)) goto all;
 //mpr=you.modem==0xFF?0:mprice[you.modem];
 hpr=BB()?(hprice[you.hd]>>1)*(float)you.hdspace/((long)hd[you.hd]<<10):hprice[you.hd]*0.9;
 do ar[i++]=ultoa(hd[i],s+i*10,10);
 while (hprice[i]<=you.money && i<7);
 ar[i]=NULL;
 q=malloc(14*14*2);
 gettext(4,11,15,24,q);
 sel:i=menuncl(10,3,0x2F,0x0F,ar,"Винты",1);
 if (i)
 {i--;
  n=1+random(echoes[3]->read/25+1);
  for (k=0;k<n;k++)
  {vars[k][1]=24576+random(8192);
   vars[k][0]=hprice[i]*(you.skill[3]>640?0.8:(1.2-you.skill[3]/1600.0))*vars[k][1]/(24576+random(8192));
   sprintf(s+70+12*k,"$%-4d  ",vars[k][0]);
   if (echoes[4]->read) sprintf(s+70+12*k+6,"  %2d%%",(dword)vars[k][1]*100/32768);
   var[k]=s+70+12*k;
  }
  var[n]=NULL;
  j=menu(10,14,0x70,0x0F,var,echoes[4]->read?" Цена  Надежн.":"Цена",1);
  if (!j) goto all1;
  decmoney(vars[--j][0]-hpr);
  //if (you.hd!=0xFF)
  chmood((i-you.hd)*(random(3)+1));
  if (hpr)
  {sprintf(s,"Ваш старый винт продан за $%d",hpr);
  message(s,0x71);
  }
  you.hd=i;you.hreli=vars[j][1];
  you.hdspace=(long)hd[you.hd]<<10;
  if (you.hdspace<os[you.os].size) {you.os=0;if (you.osreq) you.wdate=D+6;}
  if (you.soft+os[you.os].size>you.hdspace) incsoft(you.hdspace-you.soft-os[you.os].size);
  newh++;
 }
all1:puttext(4,11,15,24,q);free(q);
all:free(s);
}

void buysoft()
{char *ar[]=
 {"Антивирус","Софт для работы","Игрушки",NULL};
 char *var[5];
 int vars[5][2];	//цена, объем
 char *s=salloc(15*5);
 void *q;
 int i=0,n,k,j,cpr;
 if (Time<2*60+5) {message("Сегодня не успеем...",0x4F);goto all;}
 Time-=2*60;
 q=malloc(22*10*2);
 gettext(4,11,25,20,q);
 sel:i=menuncl(10,3,0x2F,0x0F,ar,"Виды софта",1);
 if (i)
 {i--;
  if (i==0)
  {n=1;vars[0][0]=10;vars[0][1]=0;}
  else
  n=random(5)+1;
  for (k=0;k<n;k++)
  {if (i)
   {vars[k][1]=5+random(200/i);
    vars[k][0]=Stable?(vars[k][1]*(5-i*2+random(3))/i/2.0+random(5)+1):(random(10)+10);
   }
   sprintf(s+15*k,"$%-4d  ",vars[k][0]);
   if (i) sprintf(s+15*k+6,"  %3dM",vars[k][1]);
   var[k]=s+15*k;
  }
  var[n]=NULL;
  sel1:
  j=menu(10,14,0x70,0x0F,var,i?" Цена  Объем":"Цена",1);
  if (j)
  {if (vars[--j][0]>you.money)
   {message("У вас не хватает денег",0x4F);goto sel1;}
   if (you.soft+os[you.os].size+vars[j][1]*1024L>you.hdspace)
   {message("У вас не хватает места на винте",0x4F);goto sel1;}
   decmoney(vars[j][0]);you.soft+=vars[j][1]*1024L;
   Time-=3+random(3);
   switch (i) {
    case 0: you.antiv=D;break;
    case 1: k=you.wprof?you.wprof:1;you.skill[k]+=(vars[j][1] >> 4)*(random(3));
	    break;
    case 2: chmood((vars[j][1] >> 5)*(random(3)+4));break;
   }
  }
  showstat();showtime();
  if (Time>5) goto sel;
 }
 all1:puttext(4,11,25,20,q);free(q);
all:free(s);
}

void worktime()
{int d,i,t;
 if (!you.wprof) return;
 char *s=salloc(2048);
 if (you.wtime>0) you.wdays++;
 if (D.weekday()<5)
 {if (Time>you.wtime && _rnd(you.wtime/90) && (d=_rnd(you.wtime/120))-_rnd(you.tired>>2)/2)
  {you.skill[you.wprof]+=d;
   if (!random(20))
   {if (d>0) sprintf(s,"Рост вашей квалификации не прошел незамеченным -\n        вам подняли зарплату на $%d!",d=_rnd(you.income/20)+5);
    else sprintf(s,"Усталость плохо сказывается на вашей работе.\nВаша зарплата уменьшена на $%d!",d=_rnd(you.income/20)+5);
    message(s,0x1F);
    you.income+=d;
   }
  }
  t=min(you.wtime,Time-1);
  you.tired+=_rnd(t/30)+(t>8*60?(t/30-6*2):0);
  Time-=you.wtime;
  if (Time<0)
  {i=sprintf(s,"Вы уделяете недостаточно внимания работе!");
   if (_rnd(-Time)>30) {
    d=(float)Time/2/you.wtime*you.income; //d<0
    d=(d/5)*5;
    if (d<-50 || you.income+d<50)
    {sprintf(s+i," Вы уволены!");
     fire();
    }
    else
    {sprintf(s+i,"\nВаша зарплата уменьшена на $%d",-d);
     you.income+=d;
    }
   }
   message(s,0x4F);
   Time=1;
  }
 }
 free(s);
}


void studtime()
{int t;
 float d=1.0;
 if (!you.sprof || you.sdays<0) return;
 if (D.weekday()==6 && (you.spay>0 || you.spay<0 && studper(D))) return;
 if (you.spay<0)
 {if (D==25.01 || D==25.06) //session end
  {if (you.mark<3.0)
   {message("Вы завалили сессию и отчислены из института!",0x4F);
    expel();return;
   }
   else if (you.mark<4.5)
   {message("Вы таки сдали сессию...",0x1F);you.spay=-30;chmood(5);}
   else if (you.mark<5.0)
   {message("Вы сдали сессию хорошо и заработали повышенную стипендию!",0x1F);
    you.spay=-40;chmood(10);
   }
   else
   {message("Вы сдали сессию отлично и заработали максимальную стипендию!",0x1F);
    you.spay=-50;chmood(15);
   }
  }
  if (studper(D)==2) return;
  if ((D==2.01 || D==1.06) && you.mark<2.5)
  {message("Вы даже не смогли сдать зачеты!\n Вы отчислены из института.",0x4F);
   expel();return;
  }
  t=6*60.0*(d=you.intens/100.0);
 } else t=2*60;
 if (Time<t)
 {d*=Time/t;t=Time-1;message("Вы уделяете недостаточно внимания учебе!",0x4F);}
 Time-=t;
 d/=(1+_rnd(you.tired>>2)/8.0);
 you.skill[you.sprof]+=d*(random(4));
 you.mark=(you.mark*you.sdays+4.75*d)/(you.sdays+1);you.sdays++;
 if (you.mark>5.0) you.mark=5.0; else if(you.mark<2.0) you.mark=2.0;
 you.tired+=_rnd(t/30)+(t>6*60?(t/30-6*2):0);
 chmood(-_rnd(you.tired>>2)/2);
}

void joytime()
{int i,t;
 float r;
 you.expens=-150;
 for (i=0;i<4;i++)
  if (occup[i].ord==4) break;
 if (i==3) return;i++;
 you.expens-=150/i;
 t=(_rnd(8)+1)/(i+1)*60;
 if (t>Time) r=Time/t; else r=1.0;
 chmood(_rnd(8-i)*r);
 Time-=min(Time-1,t);
}

void mailtime()
{long l;
 int i,d,k=0,lim,lost=0,traf=0;
 char *s=salloc(2048);
 for (i=0;i<10;i++)
 {bbs[i].time=bbs[i].mxtime;bbs[i].soft+=random(150*(bbs[i].modem+1));}
 for (i=0;i<E;i++)
 {if (D.day()==SD.day() && echoes[i]->stat!=2 && echoes[i]->izverg && !random(4))
  {sprintf(s,"Moderator of %s",echoes[i]->name);
   fidomess(s,"All","АМНИСТИЯ","В эхе проводится subj! Все плюсы аннулированы.");
   echoes[i]->plus=0;
  }
  if ((echoes[i]->read-=25)<0) echoes[i]->read=0;
  if (echoes[i]->stat)
  {if (!Down)
   {k++;
    if (echoes[i]->stat==2)
    {if (!echoes[i]->read) echoes[i]->traf*=(5.0-Style+random(5))/10;
     if (echoes[i]->traf<=2)
     {sprintf(s,"Модерируемая вами эха %s загнулась! Трафик упал до 0.",echoes[i]->name);
      message(s,0x4F);delecho(i);chmood(-10);chrep(-4-Style);
      block(1,24,0xF);showstat(1,22,0x30);break;
     }
    }
    else
    {if (i && (echoes[i]->traf+=random(6)-3)<=2) echoes[i]->traf=random(5)+5;
     if ((echoes[i]->mark<2 || you.points)
          && _rnd(echoes[i]->new1)+1>echoes[i]->newm)
	  echoes[i]->moderatorial();
    }
    if (i && _rnd(echoes[i]->new1)+1>echoes[i]->newm && _rnd(Style))
    {echoes[0]->msg++;echoes[0]->newm++;echoes[0]->new1++;}
    if (echodescr[i]!=NULL && echoes[i]->traf/2>=1000)
     echoes[i]->traf=1800;
    echoes[i]->newm+=echoes[i]->traf/2;
    echoes[i]->msg+=echoes[i]->traf/2;
    lim=(echoes[i]->traf/200+1)*100;
    if (echoes[i]->msg>lim) echoes[i]->msg=lim;
    if (echoes[i]->newm>lim)
    {if (echoes[i]->mark<2) lost+=echoes[i]->newm-lim;
     echoes[i]->newm=lim;
    }
    echoes[i]->new1=echoes[i]->newm;
   }
  }
  else
  {if (echoes[i]->dl==D) echoes[i]->plus=0;
   if (_rnd(you.points)>_rnd(16) && echoes[i]->plus<3 && !Down &&i>1)
   {sprintf(s,"Поинты просят подписаться на %s",echoes[i]->name);
    message(s,0x71,1+auto_[0]);
    switch (auto_[0]) {
    case 0: echlink();break;
    case 1: echlink(i);break;
    }
    if (!echoes[i]->stat)
    {d=you.points;you.points*=(8-_rnd(7))/10.0;
     echoes[1]->traf*=(float)you.points/d;
     d-=you.points;chrep(-d*(5+random(2)));}
   }
  }
 }
 if (Down) goto all;
 if (lost)
 {message("Вы не успеваете читать всю почту, и это портит вам настроение",0x4F);
   chmood(-signed((_rnd(lost)>>1)%30));
 }
 if (!chktrf(traf)) echlink();
 if (you.status && !Down)
  echread(0);
 chmood(_rnd(you.points>>3));
 if (you.sysop)
 {l=random(150*(you.modem+1));
  l=incsoft(l);
  you.virus+=random(l)<(l>>3);
  Time-=l*0.1+random(20);
  if (Time<0)
  {message("Вы не успеваете следить за своей ББС, и это портит вам настроение",0x4F);
   chmood(-signed((_rnd(-Time)>>1)%30));
   Time=1;
  }
 }
 all:free(s);
 if (Time<6*60) you.tired+=(6*60-Time)/60;
}

dword newday()
{int i,k,t,mpr,cpr;
 dword res=0;
 void *q;
 long l,b;
 char *arm[]={"Откупиться","Прятаться у друзей","Идти служить",NULL};
 char *s=salloc(2048);
 if (Time<6*60) you.tired-=(Time<6*60)/30;
 if ((you.tired-=Time/30.0*4)<=0) you.tired=0;
 else chmood(-you.tired%50);
 D+=1;
 Time=20*60;
 if (you.tired>32)
 {t=(8+random(4))*60+10+random(10)*5;
  sprintf(s,"Вы проспали %d часов %d минут!",t/60,t%60);
  Time-=t;if ((you.tired-=t/30.0*4)<=0) you.tired=0;
  message(s,0x4F);
 }
 you.money+=round(you.expens/30.0);
 if (!random(20))	 //dequalification
 {do i=random(3)+1;while (i==you.sprof || i==you.wprof);
  if (you.skill[i]>0) you.skill[i]--;
 }
 if (!random(40)) //устаревание софта
 {incsoft(-_rnd(max(you.soft >>7,min(you.soft,500))),0);}
 showtime();
 if (D.month()==1 && D.day()==1)
 {message("\n C Новым Годом! \n", 0x1F);
  for (i=0;i<10;i++) if (bbs[i].mxtime==-1) bbs[i].mxtime=0;
  Down++;chmood(random(10));
  you.tries=0;
 }
 if ((D.month()==6 || D.month()==1) && you.army==2 && D-SD>2*30) you.army=3;
 if (you.sdays==-1 && D.month()==9 && D.day()==1)
 {you.spay=-30;you.sdays=1;
  message("Вот и началась ваша учеба в институте.\nТеперь вы будете получать $30 стипендии.\nОгромные деньги, не правда ли?",0x1F);
 }
 if (D==you.grad)
 {if (you.spay<0)
  {sprintf(s,"Вас есть с чем поздравить - вы окончили институт%s!",you.mark>=4.75?" с красным дипломом":"");
   you.skill[you.sprof]+=you.mark*10;you.army=0;
   message(s,0x1F);
  }
  else {message("Вы окончили платные курсы.",0x1F);you.skill[you.sprof]+=10;}
  you.sprof=0;you.spay=0;
 }
 if (you.army==3 && (D.month()==4 || D.month()==10) && !random(7))
 {message("         Пришла повестка на бумажке!!!\nГоворила вам мама - надо в институт поступать...",0x4F);
  if (!Stable)
  {while (!(i=menu(12,25,0x70,0x0F,arm,"Варианты",1)));
   switch (i) {
    case 1:q=openbox(10,29,14,52,0x70);
	   prn(12,30,"Сколько дать? $    00");k=0;
	   i=nmbrscrl(&k,12,45,min(999,you.money/100),1,1);
           closebox(10,29,14,52,q);
	   you.money-=k*100L;
           if (_rnd(k)>=20)
           {message("Считайте, что военкомат забыл о вас навсегда!",0x1F);
            you.army=0;
           } else if (_rnd(k)>5)
           {message("Вам дали отсрочку до следующего призыва.",0x1F);
            you.army=2;
           } else
           {message("Взятка не помогла! То ли честный попался, то ли мало дали...",0x4F);
            goto oblom;
           }
           break;
    case 2:if (_rnd(you.friends))
           {message("На сей раз вы отсиделись, но друзья не могут прятать вас вечно...",0x1F);
           break;}
           else message("Увы, никто не смог вам помочь...",0x4F);
    default:goto oblom;
   }
  }
  else {oblom:block(1,24,0x4F);
   message("Вас забрали в армию. Вот, собственно, и все...",0x4F);
   quit(2);
  }
 }
 if (D.weekday()==6 && _month(D+7)!=D.month() && you.status)
  if (yn("Пойдете на сисопку?"))
  {t=min(Time-1,4*60+random(8*60));
   Time-=t;
   chmood(t/90+_rnd(you.friends));
   you.money-=_rnd(t/60);
   you.friends+=(_rnd(t/180)>0);
   message("Как ни странно, общаться можно не только по модему...",0x1F);
  }
 for (i=0;i<4;i++)
 {(occup[i].func)();
  showtime();
 }
 if (!Down && auto_[3] && you.antiv.date && D.days()>=lstscn.days()+auto_[3]) vircheck(2,4);
 if (you.spay>0 || you.spay<0 && studper(D)!=2) you.sdays++;
 if (D.day()<20 && random(10)<_rnd(you.friends) && you.money>100)
 {l=lrandom(you.money>>3)+5;
  sprintf(s,"Друг просит $%ld в долг до конца месяца. Дадите?",l);
  if (yn(s,auto_[1])) {you.money-=l;you.debt-=l;chrep(random(3)+1);}
  else
  {message("Жадность не способствует дружбе...",0x4F,1+auto_[1]);
   if (lrandom(you.money/l)>8) you.friends--;
  }
 }
 if (you.wtime>0 && D.weekday()<5)
  if (D>=you.wdate)
  {you.wdate=0;
   if (you.osreq && you.os!=you.osreq)
   {message("Вы и ваш софт не подходите для этой работы. Вы уволены!",0x4F);
    fire();
   }
   else if (_rnd(you.income)>80+(i=random(5)+1)*80 && !you.wdate.Date && (you.osreq=i)!=you.os)
   {sprintf(s,"Ваша работа требует перехода на %s\nУ вас в запасе 6 дней.",OSnames[you.osreq]);
    message(s,0x4F);you.wdate=D+6;if (auto_[2]==1) instOS(you.osreq);
   }
  }

 for (i=0;i<10;i++)
  if (!random(20)) {if (!(bbs[i].down=!bbs[i].down)) bbs[i].modem=random(6);}
 //             disasters begin
 if (!Stable)
 {if (!random(60) && you.money>300)
  {sprintf(s,"Из-за финансового кризиса вы потеряли $%ld",l=lrandom(you.money>>1)+50);
   message(s,0x4F); chmood(-l/you.money*32.0);you.money-=l;
  }
  if (you.wprof)
   if (!random(50))
   {message("Из-за экономического кризиса ваша фирма лопнула,\n      и вы потеряли работу!",0x4F);
    you.wdays=0;chmood(-10);newjob(0,0,0);
   }
   else if (!random(40))
   {sprintf(s,"Из-за экономического кризиса ваша зарплата уменьшена на %d%c",k=random(50)+1,'%');
    message(s,0x4F);chmood(-(k>>2));you.income*=1-k/100.0;
   }
 }
 if (!Down)
 {
  if (you.comp!=0xFF)
  {you.virus+=_rnd(you.virus+1);
   if (_rnd(you.virus>>3) && (l=_rnd(you.soft>>1)))
   {sprintf(s,"Злобные вирусы погрызли %luK вашего КРУТОГО СОФТА!",l);
    message(s,0x4F);
    chmood(-(float)l/(you.soft+1)*50*(2-(1.0+lrandom(you.soft>>9)/(1+(you.soft>>8)))));
    incsoft(-l);
   }
   if (wear(&you.hreli))
   {if (random(3))
    {if (l=_rnd(you.soft))
     {sprintf(s,"                        У вас покрылся винт!\nК счастью, не насмерть, но %luK КРУТОГО СОФТА погибли безвозвратно",l);
      message(s,0x4F);
      chmood(-(float)l/(you.soft+1)*50*(2-(1.0+lrandom(you.soft>>9)/(1+(you.soft>>8)))));
      incsoft(-l);
     }
    }
    else
    {if ((b=_rnd((long)hd[you.hd] << 6))>you.hdspace-(3<<10)) b=you.hdspace-(3<<10);
     b=(b>>2)<<2; //block=4K
     if (b)
     {l=you.soft*(float)b/you.hdspace;
      i=sprintf(s,"У вас посыпался винт! %luK ушло в бэд блоки.",b);
      if (l) sprintf(s+i,"\n%luK КРУТОГО СОФТА погибли безвозвратно.",l);
      message(s,0x4F);
      you.hdspace-=b;
      chmood(-(float)l/(you.soft+1)*50*(2-(1.0+lrandom(you.soft>>9)/(1+(you.soft>>8)))));
      incsoft(-l);
     }
    }
    if (you.hdspace<os[you.os].size || l>(you.soft>>1))
    {sprintf(s,"Порушилась операционная система...\nГрузим с дискетки %s",OSnames[0]);
     message(s,0x4F);chmood(-signed(_rnd(you.os+1)));
     you.os=0;Time-=os[0].itime;if (Time<1) {Time=1;chmood(-2);}
     if (you.osreq) you.wdate=D+6;
    }
   }
   else if (wear(&you.creli))
    switch (random(5)) {
    case 0:k=random(7)+1;
           sprintf(s,"Сегодня черный день в вашей жизни! Скончался ваш компьютер...\n      Вы в трауре, станция в дауне на  %d %s...",k,end(k,end2));
	   message(s,0x4F);
	   chmood(-8*(you.comp+1));
	   Down+=k;you.comp=0xFF;setbit(res,1);buycomp(k);
	   break;
    case 1:case 2:
    case 3:i=random(cprice[you.comp])+1;
	   sprintf(s,"  Вашему компьютеру потребовался ремонт.\nЭто обошлось вам в $%d и %d дня дауна...",
		   i,k=random(3)+2);
	   message(s,0x4F);
	   Down+=k;
	   if (decmoney(i)) chmood(-10);
	   else chmood(-i*50/(you.money+i));
	   break;
    }
   else if (wear(&you.mreli))
   {k=random(4)+1;
    sprintf(s,"Горе-то какое... Модем у вас сгорел, однако!\nВаша станция в дауне на %d %s...",k,end(k,end2));
    message(s,0x4F);Down+=k;
    chmood(-4*(you.modem+1));you.modem=0xFF;setbit(res,0);buymodem(k);
   }
  }
 }
 //                 disasters end
 // month ends
 if (D.day()==SD.day())
 {if (you.wdays<30)
  {if (you.wdays>=7)
   {you.money+=you.income*(float)(you.wdays%30)/30;}
  }
  else
  {you.money+=you.income;}
  you.money-=you.spay;
  if (you.debt<0)	 //должны тебе
  {if (random_(you.reput/8)>you.friends) l=you.debt;
   else
   {l=-lrandom(-you.debt)-1;message("Вам вернули только часть долга...",0x4F);}
   you.money-=l;you.debt-=l;
  }
  else if (you.debt)	//должен ты
  {if (you.money<you.debt)
   {l=max(you.money,0);
    message("Вы не вернули долг! Это портит репутацию и отношения с друзьями",0x4F);
    chrep(-((you.debt-l)>>2));
    if((you.friends-=(you.debt-l>30))<=0)
     {you.friends=0;chrep(-10);}
   }
   else i=you.debt;
   you.money-=i;you.debt-=i;
  }
  if (you.money<0)
  {mpr=you.modem==0xFF?3:mprice[you.modem]*0.8;
   cpr=you.comp==0xFF?15:cprice[you.comp]*0.8;
   you.money+=mpr;you.modem=0xFF;
   setbit(res,0);
   i=sprintf(s,"ФИДО, конечно, штука хорошая, но деньги иногда зарабатывать тоже надо.\n  Вам пришлось продать %sмодем, чтобы не умереть с голоду...",
	     you.money>=0?"":"компьютер и ");
   if (you.money<0) {you.money+=cpr;you.comp=0xFF;setbit(res,1);}
   if (you.money<cprice[0]+mprice[0])
   {sprintf(s+i,"\n и даже это вам не помогло! Вот, собственно, и все...");
    block(1,24,0x4F);
   }
   else {sprintf(s+i,"\n После уплаты долгов у вас осталось $%ld",you.money);}
   message(s,0x4F);
   Down=8;
   if (you.money<cprice[0]+mprice[0]) quit(1);
   else {buymodem();if (you.comp==0xFF) buycomp();}
   Down=0;
  }
 }
 free(s);
 showstat(1,22,0x30);
 if (Down) Down--;
 return res;
}

void initech()
{int i;
 echoes[0]=new netmail;
 echoes[1]=new local;
 echoes[2]=new point;
 echoes[3]=new exch;
 echoes[4]=new bllog;
 echoes[5]=new ruanekdot;
 echoes[6]=new job;
 echoes[7]=new vcool;
 echoes[8]=new hardw;
 echoes[9]=new softw;
 echoes[10]=new fecho;
}

main(int argc,char **argv)
{void *q;
 char *s=salloc(1024);
 char *help=salloc(15*1024);
 int i,j,k,m,y,x,sel;
 long l;
 char c;
 list tl;
 toccup tmp;
 char *upgrm[]={"Компьютер","Модем","Винт","Себя",NULL};
 char *emenu[]={"GoldEd","Подписка","Создание","Поведение в эхах","Статистика",NULL};
 char *points[]={"Набрать","Разогнать",NULL};
 char *game[]={"Save","Log on","View ReadMe","Quit to DOS",NULL};
 char *logst[]={"Log on","Log off"};
 char *bbsmenu[]={"Звонить",NULL,NULL};
 char *tmenu[]={"Приоритеты","Развлечься","Автопилот",NULL};
 char *smenu[]={"Антивирус","Операционная система","Купить","Расчистить", NULL};
 char *jmenu[]={"Устроиться","Уволиться",NULL};
 char *lmenu[]={"Поступить в институт","Поступить на курсы","Интенсивность занятий","Бросить учебу", NULL};
 char *fmenu[]={"Пообщаться","Попросить взаймы",NULL};
 char *aut[]={"Подписываться ","Давать в долг ","Ставить ОС    ",NULL};
 char *autop[]={"Вручную","Да     ","Нет    ",NULL};

 byte *buf;
 if (setvesa640x480x256())
 {if (loadbmp("fidologo.bmp",&buf))
  {free(buf);
   getch();
  }
 }
 textmode();
 textattr(0x0F);clrscr();
 lstscn=0;
// errlog=fopen("errlog","w+t");fclose(errlog);
 log=fopen("log","a+t");

 srand(loww(0x46C));
 prnc(0,0," FIDO v.1.8 (C) YuN 1997-99  │                                                    ",0x1F);
 block(1,24,0xF);cursoff();
 if (i=loadfile("readme.fid",help)) help[i]=0;
 else {message("Не найден Readme.fid! Так дело не пойдет!",0x4F);quit(10);}
 if (--argc) {setpref(echoname);initech();
  if (!load()) {sprintf(s,"Ошибка чтения! Видать, не судьба...\nerror code %d  coreleft()=%lu",errno,coreleft());
                       message(s,0x4F);quit(10);}
 }
 else
 {SD=getcurdate();SD.setday(1);
  memset(you.name,' ',30);you.name[0]=0;
  q=openbox(10,15,14,65,0x71);
  prn(11,17,"Введите ваше настоящее имя (латинскими буквами)");
  prnc(12,25,you.name,0x0F);
  gotoyx(12,25);input(you.name,29);
  for (i=0;i<22;i++) cityname[i]=cities[i].name;
  cityname[i]=NULL;
  City=22;
  if (i=menu(0,50,0x70,0x0F,cityname,"Ваш город",1))
  {pref=cities[City=--i].pref;}
  else
  {prn(13,17,"Префикс вашего города:");prnc(13,42,pref,0x0F);
   gotoyx(13,42);input(pref,8);
  }
  setpref(echoname);
  if (i=menu(1,0,0x70,0x0F,month,"Месяц",1)) SD.setmonth(i);
  D=SD;
  Stable=menu(6,20,0x70,0x0F,situat,"Обстановка в стране",1);
  if (Stable) Stable--;
  i=menu(14,20,0x70,0x0F,profn+1,"Специализация",1);
  you.skill[i]=10;
  switch(i) {
   case 1:you.soft=2048;break;
   case 2:you.comp=1;break;
   case 3:you.money=400;break;
  }
  closebox(10,15,14,65,q);
  initech();
  q=openbox(10,10,15,70,0x71);
  write(11,12,"Вы, наверное, думаете, что вот так сразу и попали в ФИДО?\nКак бы не так! Вас пустишь, а вы начнете флеймить и ламер-\nствовать! А это право надо еще заслужить!\nИтак, вы начинаете в качестве юзера BBS...");
  anykey();
  closebox(10,10,15,70,q);
  for (i=0;i<10;i++)
  {bbs[i].time=bbs[i].U=bbs[i].D=0;
   bbs[i].soft=random(20000);
   bbs[i].name=bbsnames[i];
   bbs[i].modem=random(6);
   bbs[i].down=random(7)?0:1;
   for (k=0;k<LE-2;k++)
    if (random(3)) bbs[i].ech[k]=1;
  }
  Time=you.ftime;
 }
 showstat(1,22,0x30);
 game[1]=logst[Log];
 while (1)
 {while (Down) newday();
  showhelp();
//elog("main cycle");
  l0:c=getch();if (!c) goto l0;
  switch (upcase(c)) {
   case 'B':bbsmenu[1]=you.sysop?"Прибить":"Создать";
	    i=menu(12,25,0x70,0x0F,bbsmenu,"BBS",1);
	    switch (i) {
	     case 1: gettext(1,15,21,21,q=malloc(7*22*2));
		     i=menuf(1,0,0x2F,0x0F,bbsnames,"BBS",LastBBS+1,&BBSinfo);
		     puttext(1,15,21,21,q);
		     free(q);
		     if (i) callBBS(i-1);
		     break;
	     case 2:if ((k=you.modem+(you.soft>>12))>20) k=20;
		    if (!you.sysop) {
		     q=openbox(10,21,14,59,0x70);
		     prn(12,24,"Название BBS");
		     prnc(12,39,bbsnames[11],0x0F);gotoyx(12,39);
		     if (input(bbsnames[11],18))
		     {you.sysop=1;chrep(k);}
		     closebox(10,21,14,59,q);
		    }
		    else
		    {you.sysop=0;chrep(-k);
		     sprintf(s,"%s BBS ликвидирована.\nНо вас еще долго будут доставать модемными\nзвонками, и это портит вам настроение.",bbsnames[11]);
		     message(s,0x4F);
		     chmood(-signed(_rnd(k >> 1))-3);
		    }
		    break;
	    }
	    break;
   case 'S':i=menu(12,25,0x70,0x0F,smenu,"Soft",1);
	    switch (i) {
	     case 1:vircheck(2,4);break;
	     case 2:instOS();break;
	     case 3:buysoft();
		    break;
	     case 4:q=openbox(10,23,14,55,0x70);
		    prn(12,25,"Сколько % софта оставить:");
		    k=100;
		    nmbrscrl(&k,12,50,100);
		    you.soft*=k/100.0;
		    closebox(10,23,14,55,q);
		    break;
	    }
	    break;
   case 'J':i=(you.wtime?menu(12,25,0x70,0x0F,jmenu,"Работа",1):1);
	    switch (i)
	    {case 1:joffer();break;
	     case 2:newjob(0,0,0);break;
	    }
	    break;
   case 'L':if (!(i=menu(12,25,0x70,0x0F,lmenu,"Учеба",1))) break;
	    if (i<3 && !(k=menu(12,25,0x70,0x0F,profn+1,"Профиль",1))) break;
	    switch (i)
	    {case 1:if (D.month()!=6) message("Вступительные экзамены будут в июне!",0x4F);
		    else
		    if (you.tries>3) message("Попытайте счастья через год!",0x4F);
		    else
		    {if (_rnd(you.skill[k])<30)
		     {message("Вы не набрали проходной балл",0x4F);you.tries++;}
		     else
		     {you.sdays=-1;you.sprof=k;if (you.army) you.army=1;
		      you.grad.setdate(20,5,D.year()+4);
		      sprintf(s,"Ну вот вы и студент! Учеба начнется 1 сентября и закончится в мае %d.\n         Если вас не выгонят раньше, разумеется.",you.grad.year());
		      message(s,0x1F);
		     }
		     newday();
		    }
		     break;
	     case 2:if (you.money<100) {message("У вас нет даже $100 на первый взнос",0x4F);break;}
		    you.money-=100;you.spay=100;you.sdays=1;
                    if (you.army==1) you.army=3;
		    you.grad.setdate(D.day(),D.month()+3,D.year());
		    message("Окончание учебы через 3 месяца",0x1F);
		    you.sprof=k;
		    break;
             case 3:q=openbox(10,20,14,60,0x70);
		    prn(12,21,"Интенсивность учебы в ВУЗе      %");
		    nmbrscrl(&you.intens,12,49,200,10,10);
		    closebox(10,20,14,60,q);
		    break;
	     case 4:you.spay=0;you.sdays=0;you.grad=0;you.sprof=0;
                    if (you.army==1) you.army=3;
	    }
	    break;
   case 'P':if (you.status>1)
	    {i=menu(12,25,0x70,0x0F,points,"Поинты",1);
	     switch (i)
	     {case 1:if (!echoes[2]->stat)
		     {sprintf(s,"Подпишитесь на эху %s",echoes[2]->name);
		      message(s,0x4F);break;}
		     q=openbox(10,23,14,55,0x70);
		     prn(12,25,"Сколько поинтов набрать:");
		     nmbrscrl(&maxpnt,12,50,64,you.points);
		     closebox(10,23,14,55,q);
		     break;
	      case 2:q=openbox(10,23,14,57,0x70);
		     prn(12,25,"Сколько поинтов оставить:");
		     k=you.points;
		     chrep(nmbrscrl(&you.points,12,50,you.points)*(4+random(3)));
		     if (k) echoes[1]->traf*=(float)you.points/k;
		     maxpnt=0;
		     closebox(10,23,14,57,q);
		     break;
	     }
	    }
	    break;
   case 'F':if (!you.friends) break;
	    i=menu(12,25,0x70,0x0F,fmenu,"Друзья",1);
	    switch (i) {
	     case 1:if (Time<=30) {message("Увы, у вас нет на это времени...",0x4F);break;}
		    j=_rnd(Time-30)+30;Time-=j;
		    chmood(j/90+_rnd(you.friends));
		    message("Как ни странно, общаться можно не только по модему...",0x1F);
		    break;
	     case 2:l=(you.money-you.debt*3+(you.reput>>3))/4*you.friends;
		    if (l>0) l=l/2+lrandom(l/2);
		    if (l<=5) message("Увы, сейчас друзья не могут вам помочь...",0x4F);
		    else
		    {sprintf(s,"Вы взяли взаймы $%ld до конца месяца",l);
		     message(s,0x1F);
		     you.money+=l;you.debt+=l;
		    }
	    }
	    break;
   case 'E':if (you.status) {
	     i=menu(12,25,0x70,0x0F,emenu,"Эхоконференции",1);
	     switch (i) {
	      case 1:echread(1);break;
	      case 2:echlink();break;
	      case 3:if (you.moder>3)
		     {message("Вы хотите модерировать слишком много конференций!",0x4F);
		      break;
		     }
		     q=openbox(10,13,15,68,0x70);
		     echoes[E]=new echo(E);
		     prn(12,14,"Название конференции");
		     prnc(12,36,echoes[E]->name,0x0F);gotoyx(12,36);
		     if (!input(echoes[E]->name,29) || !echoes[E]->name[0])
		     {free(echoes[E]->name);echoname[E]=NULL;
		      delete echoes[E];
		     }
		     else
		     {prn(13,14,"Описание конференции");
		      prnc(13,37,echodescr[E],0x0F);
		      gotoyx(13,37);input(echodescr[E],29);
		      for (i=0;echoname[E][i];i++)
		       echoname[E][i]=upcase(echoname[E][i]);
		      echoes[E]->stat=2;you.moder++;E++;chrep(4);
		     }
		     closebox(10,13,15,68,q);
		     break;
	      case 4:i=menu(12,25,0x70,0x0F,style,"Ваш стиль",Style+1);
		     if (i) Style=i-1;
		     break;
	      case 5:q=openbox(4,5,22,75,0x70);
		     prn(4,13,"Эха");prn(4,37,"Трафик,К");
		     prn(4,46,"Время,мин");prn(4,60,"Награды");
		     for (i=k=l=m=0;i<E;i++)
		      if (echoes[i]->stat && echoes[i]->mark<2)
		      {sprintf(s,"%-30s  %4d      %3d",
			       echoes[i]->name,echoes[i]->traf,echtime(i));
		       l+=echoes[i]->traf;m+=echtime(i);
		       prn(5+k,7,s);
		       for (j=0;j<echoes[i]->plus;j++)
			prn(5+k,60+(j<<2),"[+]");
		       k++;
		      }
		     sprintf(s,"             Всего              %4ld    %d ч.%02d мин.",l,m/60,m%60);
		     prn(21,6,s);
		     anykey();
		     closebox(4,5,22,75,q);
	     }
	    }
	    break;
   case 'U':switch(menu(12,25,0x70,0x0F,upgrm,"Что апгрейдим?",1)) {
	    case 1:buycomp();break;
	    case 2:buymodem();break;
	    case 3:buyhd();break;
	    case 4:switch (you.status) {
		   case 0:if (!newinfo(2))
			  {sprintf(s,"Читайте эху %s",echoes[2]->name);
			   message(s,0x4F);break;}
			  if (you.reput>32) {
			   q=openbox(10,14,10+7,14+50,0x0F);
			   prn(10,30,"Экзамен по полиси");
			   for (i=0;i<9;i++) qstns[i].mark=0;
			   for (i=0;i<3;i++)
			    if (!test(qstns,9,10,14)) break;
			   closebox(10,14,10+7,14+50,q);
			   if (i<3) {message("Учите полиси!",0x4F);goto ref;}
			   message("Вы получили поинтовый адрес! Теперь вы фидошник. Вам больше не надо\nчитать почту с ББС, вы можете подписываться на эхи и даже создавать\nсвои собственные. Но чтобы стать полноправным членом ФИДО, вам надо\nполучить нодовый адрес.",0x1F);
			   chmood(++you.status*2);
			   for(i=2;i<=LE;i++) echoes[i]->stat=0;
			   echoes[0]->stat=echoes[1]->stat=1;
			  }
			  else
			   ref:message("Никто не хочет брать вас поинтом",0x4F);
			  break;
		   case 1:if (you.reput>128) {
			  y=1;x=1;
			  q=openbox(y,x,y+22,x+46,0x1E);
			  prn(y,x+12,"Укажите пункты заявки");
			  for (k=0;k<30;k++)
			  {i=random(21);j=random(21);
			   tl=ndreq[i];ndreq[i]=ndreq[j];ndreq[j]=tl;
			  }
			  for (i=0;i<21;i++)
			  {ndreq[i].mark=0;prn(y+1+i,x+2,ndreq[i].str);}
			  sel=0;
			  select:
			   for(i=x+2;i<x+44;i++) scra(y+1+sel,i,0x0F);
			  do c=getch();while (!c);
			  switch (c) {
			   case 27:c=0;goto all;
			   case 13:c=1;goto all;
			   case 32:ndreq[sel].mark^=1;
				 scrs(y+1+sel,x+1,ndreq[sel].mark?'√':' ');
				 break;
			   case 73:/*PgUp*/
				 if (sel>0) {for(i=x+2;i<x+44;i++) scra(y+1+sel,i,0x1E);sel=0;}
				 break;
			   case 81:/*PgDn*/;
				 if (sel<20) {for(i=x+2;i<x+44;i++) scra(y+1+sel,i,0x1E);sel=20;}
				 break;
			   case 72:for(i=x+2;i<x+44;i++) scra(y+1+sel,i,0x1E);
				 sel==0?sel=20:sel--;break;
			   case 80:for(i=x+2;i<x+44;i++) scra(y+1+sel,i,0x1E);
				 sel==20?sel=0:sel++;break;
			   }
			   goto select;
			   all:closebox(y,x,y+22,x+46,q);
			   if (!c) break;
			   for (i=0;i<21;i++)
			    if (ndreq[i].mark^ndreq[i].correct)
			    {message("Неправильно составлена заявка",0x4F);
			     goto ref1;
			    }
			   message("Вы получили нодовый адрес! Теперь вы полноправный член ФИДО.\nМожете набирать поинтов, только помните, что вы отвечаете за\nих письма с вашего узла.",0x1F);
			   chmood(++you.status*2);
			   echoes[1]->traf=0;echoes[1]->stat=1;
			  }
			  else
			   ref1:message("Вам отказано в получении нодового адреса",0x4F);
			  break;
		   case 2: if (D.month()!=5)
			   {message("Выборы NC будут в мае",0x4F);break;}
			   if (you.reput>1000) {
			    chmood(++you.status*2);showstat(1,22,0x30);
			    final("          Вы избраны сетевым координатором! Поздравляю!\nПуть от юзера до NC занял у вас ");
			   }
			   else message("Ваша кандидатура не прошла на выборах NC",0x4F);
		   }
	    } break;
   case 'T':i=menu(12,25,0x70,0x0F,tmenu,"Времяпровождение",1);
	    switch (i) {
	    case 1:
		   prncc(24,0,"\x04 Enter\xFF\ Swap │ \x04 Esc\xFF\ Exit                                                         ",0x70);
		   q=openbox(10,30,15,50,0x70);
		   for(i=0;i<4;i++) prn(11+i,32,occup[i].name);
		   i=1;
		   tlbl:
		   prnc(10+i,32,occup[i-1].name,0x0F);
		   prnc(11+i,32,occup[i].name,0x0F);
		   do c=getch();while (!c);
		   switch (c) {
		    case 13:tmp=occup[i-1];occup[i-1]=occup[i];occup[i]=tmp;
			    break;
		    case 27:closebox(10,30,15,50,q);
			    showhelp();
			    goto all1;
		    case 72:prnc(10+i,32,occup[i-1].name,0x70);
			    prnc(11+i,32,occup[i].name,0x70);
		       i==1?i=3:i--;break;
		    case 80:prnc(10+i,32,occup[i-1].name,0x70);
			    prnc(11+i,32,occup[i].name,0x70);
		       i==3?i=1:i++;break;
		    }
		    goto tlbl;
	    case 2:if (you.money<5)
		    message("С такими финансами не до развлечений...",0x4F);
		   else {
		    k=5;
		    q=openbox(10,24,15,56,0x70);
		    prn(11,26,"На какую сумму развлекаемся?");
		    scrs(13,37,'$');
		    i=nmbrscrl(&k,13,38,min(you.money,999),5);
		    closebox(10,24,15,56,q);
		    if (!i) break;
		    you.money-=k;
		    if (k>64) i=(k>>6)+_rnd(k>>5); else i=1;
		    Down+=i;
		    sprintf(s,"Станция в дауне на %d %s",i,end(i,end2));
		    message(s,0x71);
		    while (Down) newday();
		    chmood((k>>3)+_rnd(k>>2)+1);
		    if (i>4 && you.wtime>0)
		    {message("Развлекаясь, вы совсем забросили работу... и потеряли ее!",0x4F);
		     fire();
		    }
		   } break;
            case 3:q=openbox(10,28,15,52,0x70);
                   for(i=0;i<3;i++)
                   {prn(11+i,30,aut[i]);prn(11+i,30+14,autop[auto_[i]]);}
                   sprintf(s,"Антивирус     %2d д.",auto_[3]);
                   prn(14,30,s);
                   i=0;
                   autl:
		   chatr(11+i,30+14,7,0x0F);
		   do c=getch();while (!c);
		   switch (c) {
		    case 13:if (i<3) {
                             if (k=menu(10+i,30+13,0x70,0x0F,autop,NULL,1))
                             {k--;auto_[i]=k;prn(11+i,30+14,autop[auto_[i]]);}
                            }
                            else
                            {sprintf(s,"%2d",auto_[3]);
                             gotoxy(45,15);
                             if (input(s,2))
                             {auto_[3]=atoi(s);sprintf(s,"%2d",auto_[3]);
                              prn(14,30+14,s);
                             }
                            }
			    break;
		    case 27:closebox(10,28,15,51,q);
			    showhelp();
			    goto all1;
		    case 72:chatr(11+i,30+14,7,0x70);
		       i==0?i=3:i--;break;
		    case 80:chatr(11+i,30+14,7,0x70);
		       i==3?i=0:i++;break;
		    }
		   goto autl;
                   break;
	    }
	    all1:break;
   case 'N':newday();break;
   case 'Y':if (strcmp(you.name,"Yuri Nesterenko")) break;
	    i=0;
	    do
	    {s[i++]=c=getch();
	    }
	    while (c!=13 && i<10);
	    s[--i]=0;
	    if (!strcmp(s,"rulez")) you.money+=1000;
	    else
	    if (!strcmp(s,"cool")) you.reput+=100;
	    else
	    if (!strcmp(s,"monster"))
	     for (i=1;i<4;i++) you.skill[i]+=100;
	    break;
   case 'G':i=menu(12,25,0x70,0x0F,game,"",1);
	    switch (i) {
	     case 1: if (D.weekday()!=6)
                     {sprintf(s,"                 Сегодня не воскресенье!\nВы можете записаться, но ваша репутация уменьшится на %d.",k=(6-D.weekday())*10);
                      if (!yn(s)) break;
                      chrep(-k);
                     }
                     if (!save("fido.dat"))
                       {sprintf(s,"Ошибка записи! Видать, не судьба...\nerror code %d  coreleft()=%lu",errno,coreleft());
                        message(s,0x4F);
                        if (save("reserve.dat")) message("Игра успешно сохранена в reserve.dat",0x1F);
                        else {sprintf(s,"Записаться в reserve.dat тоже не удалось...\nerror code %d  coreleft()=%lu\nСообщите эти цифры автору!\n",errno,coreleft());
                        message(s,0x4F);}
                       }
                       break;
	     case 2:Log=!Log;game[1]=logst[Log];break;
	     case 3:viewstr(help);break;
	     case 4:quit(0);
	    }
	    break;
   case 'W':chrep((D.weekday()-6)*10);save("fido.dat");
   case 'Q':quit(0);
  }
  block(1,24,0xF);
  if (!Time) newday();
  showstat(1,22,0x30);
 }
}
