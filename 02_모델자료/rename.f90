program test
character(len=40) :: ci,co
character(len=85) :: tline
open(1,file='total.info')
do
  read(1,*,end=10) ci,co
  open(2,file='./Input/'//trim(ci)//'.dat')
  open(3,file='./Output/'//trim(co)//'.dat')
  do 
    read(2,'(a85)',end=11) tline
	!if('03'.eq.tline(10:11)) then
	write(3,'(a85)') tline
	!endif
	
  enddo
  11 continue
  close(2)
  close(3)
enddo
10 continue
endprogram test