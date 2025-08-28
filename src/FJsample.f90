module FJsample
   use FJsample__types, only: WP, WC, C_DOUBLE, C_DOUBLE_COMPLEX, C_INT
   use FJsample__jack, only: Complement, jackError
   use FJsample__boot, only: bootComplement, stdDev, initRandom
   implicit none(external)
   private

   public :: say_hello
   public :: Complement, jackError
   public :: WP, WC, C_DOUBLE, C_DOUBLE_COMPLEX, C_INT
   public :: bootComplement, stdDev, initRandom
contains
   subroutine say_hello
      print *, "Hello, FJsample!"
   end subroutine say_hello
end module FJsample
