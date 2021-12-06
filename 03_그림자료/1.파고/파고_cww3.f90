character*20 ci,co
character*30 dum0,dum1
character*30 dum2,t1,t2
real d0,d1,d2
open(1,file='파고.inp')
do
  read(1,*,end=10) co
  open(2,file='./그림/'//trim(co)//'.dat')
  open(3,file='../../02_모델자료_cww3/Output/'//trim(co)//'.dat')
  open(4,file='./그림2/'//trim(co)//'.dat')
  do i=1,4 ; read(3,*) ; enddo
    do
      read(2,*,end=11) dum0,d1,d0,d0
      read(3,*,end=12) dum2,d2
      if(d1.le.-90.0)then      
        write(4,'(a20,a12,1f12.3,a12)') dum2,'-99.0',d2,'-99.0'
      else
		write(4,'(a20,3f12.3)') dum2,d1,d2,d2-d1
      endif
        read(2,*)
        read(2,*)

    enddo
    12 continue
    11 continue
  close(2)
  close(3)
  close(4)
enddo
10 continue

end