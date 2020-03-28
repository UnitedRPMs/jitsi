#!/usr/bin/bash

CLIENTARGS=""
uname -m | grep i686 && CLIENTARGS="-client -Xmx256m"

if [[ -n ${JAVA_HOME} ]]; then
  JAVABIN="${JAVA_HOME}/bin/java"
else
  JAVABIN="java"
fi

if ! ${JAVABIN} -version 2>&1 | grep version | grep -q 1.8; then
  if command -v zenity > /dev/null; then
    zenity --error --no-wrap --text="Your java version is $(${JAVABIN} -version 2>&1 | grep version) but you need Java JRE/JDK 1.8\nPlease install Java 1.8 or set your PATH to the right binary\nMore info: https://docs.fedoraproject.org/en-US/quick-docs/installing-java/"
  elif command -v kdialog > /dev/null; then
    kdialog --sorry "Your java version is $(${JAVABIN} -version 2>&1 | grep version) but you need Java JRE/JDK 1.8\nPlease install Java 1.8 or set your PATH to the right binary\nMore info: https://docs.fedoraproject.org/en-US/quick-docs/installing-java/" --title="Invalid Java version"
  elif command -v xmessage > /dev/null; then
    xmessage -center "$(echo -e "Your java version is $(${JAVABIN} -version 2>&1 | grep version) but you need Java JRE/JDK 1.8\nPlease install Java 1.8 or set your PATH to the right binary\nMore info: https://docs.fedoraproject.org/en-US/quick-docs/installing-java/")"
  else
    echo -e "Your java version is $(${JAVABIN} -version 2>&1 | grep version) but you need Java JRE/JDK 1.8\nPlease install Java 1.8 or set your PATH to the right binary\nMore info: https://docs.fedoraproject.org/en-US/quick-docs/installing-java/"
  fi
  exit 1
fi

if [ `getconf LONG_BIT` = "64" ]; then
SCDIR=/usr/lib64/jitsi
else
SCDIR=/usr/lib/jitsi
fi
LIBPATH="${SCDIR}/lib"
CLASSPATH="${LIBPATH}/felix.jar:${SCDIR}/sc-bundles/sc-launcher.jar:${SCDIR}/sc-bundles/util.jar:${SCDIR}/sc-bundles/dnsjava.jar:${LIBPATH}"
FELIX_CONFIG="${LIBPATH}/felix.client.run.properties"
LOG_CONFIG="${LIBPATH}/logging.properties"
COMMAND="${JAVABIN} ${CLIENTARGS} -classpath ${CLASSPATH} -Djna.library.path=${LIBPATH}/native -Dfelix.config.properties=file:${FELIX_CONFIG} -Djava.util.logging.config.file=${LOG_CONFIG} net.java.sip.communicator.launcher.SIPCommunicator"

export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:${LIBPATH}/native"

cd "${SCDIR}"

exec ${COMMAND} $*
