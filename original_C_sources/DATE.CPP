typedef unsigned int word;
typedef unsigned char byte;
#ifdef __DOS_H
#define date Date
#endif

long round(float f)
{return long(f+(f>0?.5:-.5));}

word mofs[]={0,
	     31,
	     31+28,
	     31+28+31,
	     31+28+31+30,
	     31+28+31+30+31,
	     31+28+31+30+31+30,
	     31+28+31+30+31+30+31,
	     31+28+31+30+31+30+31+31,
	     31+28+31+30+31+30+31+31+30,
	     31+28+31+30+31+30+31+31+30+31,
	     31+28+31+30+31+30+31+31+30+31+30
//	    ,31+28+31+30+31+30+31+31+30+31+30+31
	    };
struct date {
 word Date;
 word year();
 word year_();
 byte month();
 byte day();
 word setyear(word year);
 word setmonth(word month);
 word setday(byte day);
 word setdate(byte day,word month,word year);
 word days();
 byte weekday();
 byte daysinmonth();
 word operator -= (word d);
 word operator += (word d);
 word operator = (word d);
// date(byte day=0,word month=0,word year=0);
};

/*date::date(byte day,word month,word year)
{setdate(day,month,year);}
*/

word _year(word Date)
{return ((Date & 0xFE00) >> 9)+1980;}

byte _month(word Date)
{return (Date & 0x01E0) >> 5;}

byte _day(word Date)
{return Date & 0x001F;}

word date::year()
{return _year(Date);}

byte date::month()
{return _month(Date);}

byte date::day()
{return _day(Date);}

word date::setyear(word year)
{Date&=~0xFE00;
 return (Date^=(year-1980) << 9);}

word date::year_()
{return (Date & 0xFE00) >> 9;}

word date::setmonth(word month)
{if (month>12) {setyear(_year(Date)+month/12);month=month%12+1;}
 Date&=~0x01E0;
 return Date^= month << 5;}

word date::setday(byte day)
{Date&=~0x001F;
 return Date^=day;}

word date::setdate(byte day,word month,word year)
{setyear(year);setmonth(month);setday(day);return Date;}

word date::days()
{register word y;
return day()+mofs[month()-1]+(y=year_())*365+(y+3 >> 2) //1980 is leap-year
       +(!(y & 0x0003) && month()>2);
}

word operator - (date a,date b)
{return a.days()-b.days();}

word dstodate(word days)
{word d,j,i,k,y;
 date dt;
 y=days/365.25;
 while ((d=y*365+((y+3)>>2))>=days) y--;
 d=days-d;
 if (!(y & 0x0003))	//for leap-year
  if (d==mofs[2]+1)     //29 Feb
   {dt.setmonth(2);dt.setday(29);goto l1;}
  else if (d>mofs[2]) d--;
 if (d>mofs[11]) k=11;
 else
 {i=0;j=11;
  while (j>i+1)
  {k=(i+j)>>1;
   if (d>mofs[k]) i=k;else j=k;
  }
  k=i;
 }
 dt.setmonth(k+1);
 dt.setday(d-mofs[k]);
 l1:dt.setyear(y+1980);
 return dt.Date;
}

word date::operator -= (word d)
{return Date=dstodate(days()-d);}

word date::operator += (word d)
{return Date=dstodate(days()+d);}

word date::operator = (word d)
{return Date=d;}

word operator - (date a,word d)
{return dstodate(a.days()-d);}

word operator + (date a,word d)
{return dstodate(a.days()+d);}

byte operator < (date a,date b)
{return a.days()<b.days();}
byte operator < (date a,float b)
{date x;
 x.setdate(int(b),round(int(b*1000) % 1000/10.0),a.year());
 return a<x;}

byte operator > (date a,date b)
{return a.days()>b.days();}
byte operator > (date a,float b)
{date x;
 x.setdate(int(b),round(int(b*1000) % 1000/10.0),a.year());
 return a>x;}

byte operator <= (date a,date b)
{return a.days()<=b.days();}
byte operator <= (date a,float b)
{date x;
 x.setdate(int(b),round(int(b*1000) % 1000/10.0),a.year());
 return a<=x;}

byte operator >= (date a,date b)
{return a.days()>=b.days();}
byte operator >= (date a,float b)
{date x;
 x.setdate(int(b),round(int(b*1000) % 1000/10.0),a.year());
 return a>=x;}

byte operator == (date a,date b)
{return a.Date==b.Date;}
byte operator == (date a,float b)
{return a.day()==int(b) && round(int(b*1000) % 1000/10.0)==a.month();}

byte operator != (date a,date b)
{return a.Date!=b.Date;}
byte operator != (date a,float b)
{return !(a.day()==int(b) && round(int(b*1000) % 1000/10.0)==a.month());}

byte date::weekday()
{return (days()+7)%7; //0 - Monday... 6 - Sunday
}

byte date::daysinmonth()
{register byte x=month();
 return x==12?31:(mofs[x]-mofs[x-1]);
}

word getcurdate()
{word d=0;
 asm {
 mov ah,2Ah
 int 21h
 mov byte ptr d,dl
 xor dl,dl
 shr dx,1
 shr dx,1
 shr dx,1
 or d,dx
 sub cx,1980
 xchg ch,cl
 shl ch,1
 or d,cx
 }
 return d;
}

word getfiledate(int handle)
{word d;
 asm {
 mov ax,5700h
 mov bx,handle
 int 21h
 mov d,dx
 }
 return d;
}
/*#include <stdio.h>
void main()
{date D,d1;
 word d,m,y;
 D=getcurdate();
 d1=D;
 D-=4*365;
 printf("%d/%d/%d\n",D.day(),D.month(),D.year());
 d=d1.Date;
 D=d;
 printf("%d/%d/%d\n",D.day(),D.month(),D.year());

/* printf("\nTesting...\n");
 for (y=1980;y<2100;y++)
  {for (m=1;m<=12;m++)
   for (d=1;d<=mofs[m]-mofs[m-1];d++)
   {D.setdate(d,m,y);
    D.Date=dstodate(D.days());
    if (d!=D.day() || m!=D.month() || y!=D.year())
     {printf("%u %d/%d/%d",D.days(),d,m,y);goto all;}
   }
  if (!(y & 0x0003))
  {D.setdate(29,2,y);
    D.Date=dstodate(D.days());
    if (29!=D.day() || 2!=D.month() || y!=D.year())
     {printf("%u 29/2/%d",D.days(),y);goto all;}
  }
  printf("\n%d",y);
 }*/
all:;
}*/