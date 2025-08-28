program main
   use FJsample, only: say_hello, WP, Complement, jackError, bootComplement, stdDev, initRandom
   implicit none(external)
   ! Set up sizes
   integer, parameter :: ncon = 1000
   integer, parameter :: nboot = 1000
   integer, parameter :: nsize = ncon
   ! Set up raw data
   real(kind=WP), dimension(ncon) :: raw_data
   ! Jackknife variables
   real(kind=WP), dimension(0:ncon) :: jack
   real(kind=WP) :: jackErr, bias
   ! bootStrap variables
   real(kind=WP), dimension(0:nboot) :: boot
   integer, dimension(nboot, nsize) :: bootIDs
   real(kind=WP) :: bootErr
   call say_hello()
   call initRandom(5)
   ! Just fill it with some random data
   call RANDOM_NUMBER(raw_data)
   ! Take jackknifes
   call Complement(jack(0), raw_data)
   call Complement(ncon, jack(1:), raw_data)
   call jackError(ncon, jack, jackErr, bias)
   ! Do bootstraps
   call bootComplement(ncon, nboot, nsize, boot(1:), raw_data, bootIDs)
   boot(0) = SUM(boot(1:)) / real(nboot, kind=WP)
   call stdDev(boot(1:), bootErr)
   write (*, *) 'jack'
   write (*, *) 'mean, err, bias'
   write (*, *) jack(0), jackErr, bias
   write (*, *) 'boot'
   write (*, *) 'mean, err'
   write (*, *) boot(0), bootErr

end program main
