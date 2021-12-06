character*40 ci,co
character*85 tline
open(1,file='total.info')
do
  read(1,*,end=10) ci,co
  open(2,file='./Input/'//trim(ci)//'.dat3')
  open(3,file='./Output/'//trim(co)//'.dat')
  do 
    read(2,'(a85)',end=11) tline
    write(3,'(a85)') tline
  enddo
  11 continue
  close(2)
  close(3)
enddo
10 continue
end