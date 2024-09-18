var str version = file read "${KLANG_HOME}/configurations/CurrentVersion"
var str compatcode = file read "${KLANG_HOME}/configurations/CompatibilityCode"

print "KyneLang Runtime v" + version + " Compatibility Code: " + compatcode
