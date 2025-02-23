module FJsample_c
   use FJsample, only: say_hello, Complement, jackError, C_DOUBLE, C_DOUBLE_COMPLEX, C_INT
   implicit none(external)
   private

   ! Todo: Just make this public and make fortitude-lint ignore that rule for this file
   public :: say_hello_c
   public :: Complement0_c, Complement1_c, Complement2_c, Complement3_c, jackError_WP
   public :: Complement0_wc_c, Complement1_wc_c, Complement2_wc_c, Complement3_wc_c, jackError_WC

contains
   subroutine say_hello_c()
      call say_hello()
   end subroutine say_hello_c

   ! C_DOUBLE
   subroutine Complement0_c(cset, data)
      real(kind=C_DOUBLE), intent(out) :: cset
      real(kind=C_DOUBLE), dimension(:), intent(in) :: data
      call Complement(cset, data)
   end subroutine Complement0_c
   subroutine Complement1_c(ncon, cset, data)
      integer(kind=C_INT), intent(in) :: ncon
      real(kind=C_DOUBLE), dimension(ncon), intent(out) :: cset
      real(kind=C_DOUBLE), dimension(ncon), intent(in) :: data
      call Complement(ncon, cset, data)
   end subroutine Complement1_C
   subroutine Complement2_c(ncon, cset, data, icon)
      integer(kind=C_INT), intent(in) :: ncon
      real(kind=C_DOUBLE), dimension(ncon), intent(out) :: cset
      real(kind=C_DOUBLE), dimension(ncon), intent(in) :: data
      integer(kind=C_INT), intent(in) :: icon
      call Complement(ncon, cset, data, icon)
   end subroutine Complement2_C
   subroutine Complement3_c(ncon, cset, data, icon, jcon)
      integer(kind=C_INT), intent(in) :: ncon
      real(kind=C_DOUBLE), dimension(ncon), intent(out) :: cset
      real(kind=C_DOUBLE), dimension(ncon), intent(in) :: data
      integer(kind=C_INT), intent(in) :: icon
      integer(kind=C_INT), intent(in) :: jcon
      call Complement(ncon, cset, data, icon, jcon)
   end subroutine Complement3_C

   subroutine JackError_wp(ncon, c, err, bias)
      ! This subroutine works
      ! but just rescale np.cov by (ncon - 1)
      integer(kind=C_INT), intent(in) :: ncon
      real(kind=C_DOUBLE), dimension(0:ncon), intent(in) :: c
      real(kind=C_DOUBLE), intent(out) :: err
      real(kind=C_DOUBLE), optional, intent(out) :: bias
      real(kind=C_DOUBLE) :: avg
      call jackError(ncon, c, err, bias)
   end subroutine JackError_wp

   ! C_DOUBLE_COMPLEX
   subroutine Complement0_wc_c(cset, data)
      complex(kind=C_DOUBLE_COMPLEX), intent(out) :: cset
      complex(kind=C_DOUBLE_COMPLEX), dimension(:), intent(in) :: data
      call Complement(cset, data)
   end subroutine Complement0_wc_c
   subroutine Complement1_wc_c(ncon, cset, data)
      integer(kind=C_INT), intent(in) :: ncon
      complex(kind=C_DOUBLE_COMPLEX), dimension(ncon), intent(out) :: cset
      complex(kind=C_DOUBLE_COMPLEX), dimension(ncon), intent(in) :: data
      call Complement(ncon, cset, data)
   end subroutine Complement1_Wc_C
   subroutine Complement2_wc_c(ncon, cset, data, icon)
      integer(kind=C_INT), intent(in) :: ncon
      complex(kind=C_DOUBLE_COMPLEX), dimension(ncon), intent(out) :: cset
      complex(kind=C_DOUBLE_COMPLEX), dimension(ncon), intent(in) :: data
      integer(kind=C_INT), intent(in) :: icon
      call Complement(ncon, cset, data, icon)
   end subroutine Complement2_Wc_C
   subroutine Complement3_wc_c(ncon, cset, data, icon, jcon)
      integer(kind=C_INT), intent(in) :: ncon
      complex(kind=C_DOUBLE_COMPLEX), dimension(ncon), intent(out) :: cset
      complex(kind=C_DOUBLE_COMPLEX), dimension(ncon), intent(in) :: data
      integer(kind=C_INT), intent(in) :: icon
      integer(kind=C_INT), intent(in) :: jcon
      call Complement(ncon, cset, data, icon, jcon)
   end subroutine Complement3_Wc_C

   subroutine JackError_wc_c(ncon, c, err, bias)
      ! This subroutine works
      ! but just rescale np.cov by (ncon - 1)
      integer(kind=C_INT), intent(in) :: ncon
      complex(kind=C_DOUBLE), dimension(0:ncon), intent(in) :: c
      complex(kind=C_DOUBLE), intent(out) :: err
      complex(kind=C_DOUBLE), optional, intent(out) :: bias
      complex(kind=C_DOUBLE) :: avg
      call jackError(ncon, c, err, bias)
   end subroutine JackError_wc_c

end module FJsample_c
