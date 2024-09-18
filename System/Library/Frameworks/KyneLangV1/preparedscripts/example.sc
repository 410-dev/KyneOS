// This code here is used to check the installed versions of the runtime and the scriptshell.
// runtime <version>:<compatibility code> <enforce/recommend>
//
// The compatibility code is used to determine if the runtime is compatible with the scriptshell.
// The enforce/recommend flag is used to determine if the runtime is enforced or recommended.
//    If the runtime is enforced, the scriptshell will not run if the runtime is not compatible.
//    If the runtime is recommended, the scriptshell will run, but a warning will be displayed.

runtime v1:1 enforce/recommend


print "KyneLang Script v1.0.0"

var int a = 1
var str b = "Hello, World!"
var flt c = 3.14
var bool d = true
var any e = null

print abcd
journal abcd

var flt pi = math pi
var int pi2 = math pi // This should produce error - incompatible types
var any pi3 = math pi // This should be fine

print pi
print pi2 // This should produce error - not declared
print pi3

try "math sqrt test" // Creating try block with name "math sqrt test"
var any f = math sqrt -1 // This should produce error - negative number
catch "math sqrt test" // Catching error from try block with name "math sqrt test"
print "Error: " + f
endcatch "math sqrt test" // Ending catch block with name "math sqrt test"

function add:int, int -> int {
    var int a = 1
    var int b = 2
    return a + b
}

var int sum = add 1, 2

var str content = file read "example.sc"
file write "example.sc" "Hello, World!"
file delete "example.sc"
file copy "example.sc" "example2.sc"
file move "example2.sc" "example3.sc"
file exists "example3.sc"
directory create "example"
directory delete "example"
directory exists "example"
directory list "example"
directory copy "example" "example2"
directory move "example2" "example3"

shexec stdoutcapture "echo Hello, World!"
shexec exitcapture "echo Hello, World!"

if a == 1 {
    print "a is 1"
} else {
    print "a is not 1"
}

for 0...10 i {
    print i
}

httprequest get "https://www.google.com"
