character  cc*10,name*10,date*12,hms*10,station1*10,station2*10,tt*1
integer    typ,num
!real       dum
character*4  dd,wt, ws, hs,fg1,fg2, dum

call getarg(1,cc)
open(2,file='STNINFO_2020.info')

do 
   read(2,*,end=10,err=10) name,dum,dum,dum,station1
   open(4,file='../Output/'//trim(name)//'.dat')
   open(1,file='INPUT/khoa_'//trim(cc)//'.dat')
!   open(1,file='INPUT/khoa_201904.dat')
   !print *,cc, station1
   do 
	  read(1,*,end=11) station2,date,hms, dum, dd, dd, dum, dd, dd, dum, dd, dd, dd,&
                              dd, dd, dd, dd, dd, dd, dd, dd, dd, dd, dd, dd, dd, dd,&
							  dum, dd, dd, dd, dd, dd, dd, dd, dd, dd, dd, dd, dum, dd,&
 							  dd, dd, dd, dd, dd, dd, dd, wt, dd, fg1, dum, dd, dd, dum,&
 							  dd, dd, ws, dd, fg2
      !print *, station2, date, hms, wt, fg1, ws, fg2
      if(trim(wt)=='@') wt='-99.'
      if(trim(ws)=='@') ws='-99.'
	  hs = '-99.'
	  !print *, station1, station2	  
      if(trim(station1).eq.trim(station2))then
	  	  !print *, station1, station2
        if(trim(fg1).eq.'B') wt = '-99.'
		if(trim(fg2).eq.'B') wS = '-99.'
		  write(4,'(1a12,1a5,3a7)') date,hms, ws,wt,hs
		print *, station2, date, hms, wt, ws
	  endif
   enddo
   11 continue
   close(1)
enddo
10 continue
close(2)
end