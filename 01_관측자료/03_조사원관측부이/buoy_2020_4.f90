character name*20, dum*20,ok*2, ymd*10, hms*12, fg1*2, fg2*2, fg3*2
real hsig,wtem,wspd
open(1,file='input4.inp')
do
  read(1,*,end=10) name
  print *, name
  open(3,file='../Output/'//trim(name)//'.dat')
  open(2,file='INPUT/'//trim(name)//'.txt')
  do i=1,8 ; read(2,*) ; enddo
  do
    wspd = -99.;hsig = -99.; wtem = -99.
    read(2,*,end=11) dum,dum,dum,dum,dum,dum,dum,ymd,hms,hsig,ok,fg1,dum,ok,ok,dum,ok,ok,dum,ok,ok,dum,ok,ok,&
                     wtem,ok,fg2,dum,ok,ok,dum,ok,ok,wspd,ok,fg3
	
    if(hms(4:8).eq.'00:00') then
      if(fg1.eq.'B') hsig = -99.0
	  if(fg2.eq.'B') wtem = -99.0
	  if(fg3.eq.'B') wspd = -99.0	 

	  write(3,'(a10,a3,a12,3f8.2)') ymd,'  ',hms(1:5),wspd,wtem,hsig
	endif
  enddo
  11 continue
  close(2)
  close(3)
enddo
10 continue
end