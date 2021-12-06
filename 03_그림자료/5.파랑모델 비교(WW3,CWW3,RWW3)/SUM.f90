character*20 ci,co
character*20 dum0,dum1
character*20 dum2,time1,time2
real obs,ww3,cww3,rww3
open(1,file='SUM.inp')
do 
  read(1,*,end=10) co
  open(2,file='../1.파고/그림/'//trim(co)//'.dat')
  open(3,file='../../02_모델자료_cww3/Output/'//trim(co)//'.dat')
  open(4,file='../../02_모델자료_rww3/Output/'//trim(co)//'.dat')
  open(5,file='그림/'//trim(co)//'.dat')
  do i=1,4 ; read(3,*); enddo
  do i=1,4 ; read(4,*); enddo
  do
    read(2,*,end=11) dum0,obs,ww3
    read(3,*,end=12) dum2,cww3
	read(4,*,end=13) dum2,rww3
	if(obs.eq.-99.9) then
	 write(5,'(a20,a5,3f12.3)') dum0,"NaN",ww3,cww3,rww3
	else
     write(5,'(a20,6f12.3)') dum0,obs,ww3,cww3,rww3
	endif
    read(2,*,end=11) 
    read(2,*,end=11) 
  enddo
  11 continue
  12 continue
  13 continue
  close(2)
  close(3)
  close(4)
enddo
10 continue

end