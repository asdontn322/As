 #include<stdio.h>

  #include<graphics.h>

  #include<stdlib.h>

  #include<conio.h> 

  void draw_car()

{

   int   poly1[10]={0,200,0,160,260,160,260,200,0,200};

   int poly2[10]={40,160,70,130,170,130,200,160,40,160};

   setfillstyle(SOLID_FILL,5);

   fillpoly(5,poly1);

   setfillstyle(SOLID_FILL,25);

   fillpoly(5,poly2);

   setfillstyle(SOLID_FILL,20);

   fillellipse(50,200,20,20);

   fillellipse(200,200,20,20);

}

void main()

{

   int gd=DETECT,gm,i,j;

   void*bitmap;

   initgraph(&gd,&gm,"C:\\TC\\BGI");

   draw_car();

   bitmap=malloc(imagesize(0,130,270,230));

   getimage(0,130,270,230,bitmap);

   for(i=0;!kbhit();i++)

    {

      if(i>500)i=0;

      putimage(i,130,bitmap,OR_PUT);

      setbkcolor(WHITE);

      sound(100);

      delay(8);

      putimage(i,130,bitmap,XOR_PUT);

      nosound();

    }

   closegraph();

   getch();

 }

