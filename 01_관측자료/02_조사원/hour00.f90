character cc*400,dd*6
call getarg(1,dd)

open(1,file='input/DT_STATION_'//trim(dd)//'.txt')
open(2,file='input/khoa_'//trim(dd)//'.dat')
do
   read(1,'(a400)',end=10,err=10) cc
   if(cc(26:27).eq.'00') write(2,'(a400)') cc
enddo
10 continue

end