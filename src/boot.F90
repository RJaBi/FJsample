module FJsample__boot

   use FJsample__types, only: WP, WC

   implicit none(external)
   private

   logical :: seedset = .FALSE.
   integer, parameter :: default_seed = 31542525 ! just a number

   interface bootComplement
      module procedure Complement1
      module procedure Complement1_WC
      module procedure Complement1_ncon
      module procedure Complement1_WC_ncon
      module procedure Complement1_reuse
      module procedure Complement1_WC_reuse
   end interface BootComplement

   interface stdDev
      module procedure stdDev_WP
      module procedure stdDev_WC
   end interface stdDev

   public :: bootComplement, stdDev

   public :: initRandom

contains

   subroutine initRandom(seed)
      integer, intent(in) :: seed
      integer, dimension(:), allocatable :: seedArray
      integer :: statesize
      real(kind=WP), dimension(200) :: randoms
      ! Need to get the correct length to allocate
      call RANDOM_SEED(size=statesize)
      allocate (seedArray(stateSize))
      ! Use same seed for each
      ! I think this is 'bad' but fine enough here
      seedArray = seed
      ! Set the seed
      call RANDOM_SEED(put=seedArray)
      ! call 200 random numbers to 'spin' the generator up
      call RANDOM_NUMBER(randoms)
      seedset = .TRUE.
      deallocate (seedArray)
   end subroutine initRandom

   subroutine Complement1_ncon(ncon, nboot, cset, data, sampleIDs)
      integer, intent(in) :: ncon, nboot
      real(kind=WP), dimension(nboot), intent(out) :: cset
      real(kind=WP), dimension(ncon), intent(in) :: data
      integer, dimension(nboot, ncon), intent(out) :: sampleIDs
      call Complement1(ncon, nboot, ncon, cset, data, sampleIDS)
   end subroutine Complement1_ncon

   subroutine Complement1_reuse(ncon, nboot, cset, data, sampleIDS, reuse)
      integer, intent(in) :: ncon, nboot
      real(kind=WP), dimension(nboot), intent(out) :: cset
      real(kind=WP), dimension(ncon), intent(in) :: data
      integer, dimension(nboot, nboot), intent(in) :: sampleIDs
      logical, intent(in) :: reuse
      real(kind=WP), dimension(nboot, nboot) :: randomNums
      integer :: cc, aa
      if (.NOT. reuse) then
         write (*, *) "Exiting cause this is the reuse-subroutine and you set reuse=.false."
         stop
      end if
      ! Now construct all the boot strap resamples
      cset = 0.0_WP
      ! If the compiler complains about do concurrent
      ! Remove the locality specifiers (i.e. default, shared, etc)
#ifdef LOCALITYSUPPORT
      do concurrent(aa=1:nboot, cc=1:ncon) default(none) shared(data, sampleIDs) reduce(+:cset)
#else
         do concurrent(aa=1:nboot, cc=1:ncon)
#endif
            cset(aa) = cset(aa) + data(sampleIDs(aa, cc))
         end do
         cset = cset / real(ncon, kind=WP)
         end subroutine Complement1_reuse

         subroutine Complement1(ncon, nboot, nsize, cset, data, sampleIDS)
            integer, intent(in) :: ncon, nboot, nsize
            real(kind=WP), dimension(nboot), intent(out) :: cset
            real(kind=WP), dimension(ncon), intent(in) :: data
            integer, dimension(nboot, nsize), intent(out) :: sampleIDs
            real(kind=WP), dimension(nboot, nsize) :: randomNums
            integer :: cc, aa
            ! warm up the generator
            if (.NOT. seedset) then
               call initRandom(seed=default_seed)
            end if
            call RANDOM_NUMBER(randomNums)
            ! Now need to transform the random numbers in the range 0<=x<=1
            ! to be in range 1: ncon
            sampleIDs = INT(randomNums * real(ncon, kind=WP)) + 1
            ! Now construct all the boot strap resamples
            cset = 0.0_WP
            ! If the compiler complains about do concurrent
            ! Remove the locality specifiers (i.e. default, shared, etc)
#ifdef LOCALITYSUPPORT
            do concurrent(aa=1:nboot, cc=1:nsize) default(none) shared(data, sampleIDs) reduce(+:cset)
#else
               do concurrent(aa=1:nboot, cc=1:nsize)
#endif
                  cset(aa) = cset(aa) + data(sampleIDs(aa, cc))
               end do
               cset = cset / real(nsize, kind=WP)
               end subroutine Complement1

               ! COMPLEX

               subroutine Complement1_WC_ncon(ncon, nboot, cset, data, sampleIDs)
                  integer, intent(in) :: ncon, nboot
                  complex(kind=WC), dimension(nboot), intent(out) :: cset
                  complex(kind=WC), dimension(ncon), intent(in) :: data
                  integer, dimension(nboot, ncon), intent(out) :: sampleIDs
                  call Complement1_WC(ncon, nboot, ncon, cset, data, sampleIDS)
               end subroutine Complement1_WC_ncon

               subroutine Complement1_WC_reuse(ncon, nboot, cset, data, sampleIDS, reuse)
                  integer, intent(in) :: ncon, nboot
                  complex(kind=WC), dimension(nboot), intent(out) :: cset
                  complex(kind=WC), dimension(ncon), intent(in) :: data
                  integer, dimension(nboot, nboot), intent(in) :: sampleIDs
                  logical, intent(in) :: reuse
                  real(kind=WP), dimension(nboot, nboot) :: randomNums
                  integer :: cc, aa
                  if (.NOT. reuse) then
                     write (*, *) "Exiting cause this is the reuse-subroutine and you set reuse=.false."
                     stop
                  end if
                  ! Now construct all the boot strap resamples
                  cset = 0.0_WP
                  ! If the compiler complains about do concurrent
                  ! Remove the locality specifiers (i.e. default, shared, etc)
#ifdef LOCALITYSUPPORT
                  do concurrent(aa=1:nboot, cc=1:ncon) default(none) shared(data, sampleIDs) reduce(+:cset)
#else
                     do concurrent(aa=1:nboot, cc=1:ncon)
#endif
                        cset(aa) = cset(aa) + data(sampleIDs(aa, cc))
                     end do
                     cset = cset / real(ncon, kind=WP)
                     end subroutine Complement1_WC_reuse

                     subroutine Complement1_WC(ncon, nboot, nsize, cset, data, sampleIDs)
                        integer, intent(in) :: ncon, nboot, nsize
                        complex(kind=WC), dimension(nboot), intent(out) :: cset
                        complex(kind=WC), dimension(ncon), intent(in) :: data
                        integer, dimension(nboot, nsize), intent(out) :: sampleIDs
                        real(kind=WP), dimension(nboot, nsize) :: randomNums
                        integer :: cc, aa
                        ! warm up the generator
                        if (.NOT. seedset) then
                           call initRandom(seed=default_seed)
                        end if
                        call RANDOM_NUMBER(randomNums)
                        ! Now need to transform the random numbers in the range 0<=x<=1
                        ! to be in range 1: ncon
                        sampleIDs = INT(randomNums * real(ncon, kind=WP)) + 1
                        ! Now construct all the boot strap resamples
                        cset = 0.0_WP
                        ! If the compiler complains about do concurrent
                        ! Remove the locality specifiers (i.e. default, shared, etc)
#ifdef LOCALITYSUPPORT
                        do concurrent(aa=1:nboot, cc=1:nsize) default(none) shared(data, sampleIDs) reduce(+:cset)
#else
                           do concurrent(aa=1:nboot, cc=1:nsize)
#endif
                              cset(aa) = cset(aa) + data(sampleIDs(aa, cc))
                           end do
                           cset = cset / real(nsize, kind=WP)
                           end subroutine Complement1_WC

                           ! Errors

                           subroutine stdDev_WP(c, err)
                              real(kind=WP), dimension(:), intent(in) :: c
                              real(kind=WP), intent(out) :: err
                              real(kind=WP) :: mean, N
                              N = real(SIZE(c), kind=WP)
                              mean = SUM(c) / N
                              err = SQRT(SUM((c(1:) - mean)**2.0) / N)
                           end subroutine stdDev_WP

                           subroutine stdDev_WC(c, err)
                              complex(kind=WP), dimension(:), intent(in) :: c
                              complex(kind=WP), intent(out) :: err
                              complex(kind=WP) :: mean
                              real(kind=WP) :: N
                              N = real(SIZE(c), kind=WP)
                              mean = SUM(c) / N
                              err = SQRT((SUM((c - mean))**2.0_WP) / N)
                           end subroutine stdDev_WC

                           end module FJsample__boot
