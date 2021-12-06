character*20 ci,co
character*10 dum0,dum1
character*20 dum2,t1,t2
character*4  d0
real d1,d2
open(1,file='풍속.inp')
do
  read(1,*,end=10) co
  open(2,file='../../01_관측자료/Output/'//trim(co)//'.dat')
  open(3,file='../../02_모델자료/Output/'//trim(co)//'.dat')
  open(4,file='그림/'//trim(co)//'.dat')
  do i=1,9 ; read(2,*) ; enddo
  do i=1,1 ; read(3,*) ; enddo
  do
    read(2,*,end=11) dum0,dum1,d1
    do
      read(3,*,end=12) dum2,d2
      if(dum1(2:2).eq.':') t1=trim(dum0)//'-0'//trim(dum1)
      if(dum1(2:2).ne.':') t1=trim(dum0)//'-'//trim(dum1)
      t2=dum2(1:16)
      if(t1.eq.t2)then
	    if(d1.le.-90) then 
		 write(4,'(a20,2f12.3,a12)') t2,d1,d2,'-99.0'
		 !print(t2,d1,d2)
		else
         write(4,'(a20,3f12.3)') t2,d1,d2,d2-d1
		endif
        exit
      else
        write(4,'(a20,a12,1f12.3,a12)') t2,'-99.0',d2,'-99.0'
      endif
    enddo
    12 continue
  enddo
  11 continue
  close(2)
  close(3)
  close(4)
enddo
10 continue

end