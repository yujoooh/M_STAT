character  cc*10,name*15,date*12,hms*10
integer    typ,num
real       ws,wt,hs

call getarg(1,cc)
ws=0;wt=0;hs=0
open(2,file='STNINFO_2021.info')
do 
   read(2,*,end=10,err=10) name,typ,num
   print*, name,typ,num
   open(4,file='../Output/'//trim(name)//'.dat')
   if(typ.eq.1)open(1,file='./INPUT/KMA01_'//trim(cc)//'.csv')
   if(typ.eq.2)open(1,file='./INPUT/KMA02_'//trim(cc)//'.csv')
   if(typ.eq.3)open(1,file='./INPUT/KMA03_'//trim(cc)//'.csv')
   read(1,*)
   do
      if(typ.eq.1) read(1,*,end=11,err=11) k,date,hms,ws,wt,hs
      if(typ.eq.2) read(1,*,end=11,err=11) k,date,hms,ws,wt,hs
      if(typ.eq.3) read(1,*,end=11,err=11) k,date,hms   ,wt,hs
      if(typ.eq.3) ws=-99.
      if(k.eq.num)then
        if(ws.le.0.) ws=-99.
        if(wt.le.0.) wt=-99.
        if(hs.ge.10) hs=-99.
        if(hms(3:4).eq.'00'.or.hms(4:5).eq.'00') write(4,'(1a12,1a6,3f12.4)') date,hms,ws,wt,hs
      endif
   enddo
   11 continue
   close(1)
enddo
10 continue
close(2)
end