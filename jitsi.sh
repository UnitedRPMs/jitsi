#!/usr/bin/bash

# Get architecture
ARCH=`uname -m | sed -e s/x86_64/64/ -e s/i.86/32/`

JAVA_HOME="/usr/lib/jvm/jre-1.8.0-openjdk"

if [[ -n ${JAVA_HOME} ]]; then
  javabin="${JAVA_HOME}/bin/java"
else
  javabin=`which java`
fi

# Additionnal JVM arguments
CLIENTARGS=""

if [ $ARCH -eq 32 ]
then
    CLIENTARGS="-client -Xmx256m"
fi

show_splash=true
for arg in "$@" ; do
  if [ "$arg" = "--splash=no" ] ; then
    show_splash=false
  elif [ "$arg" = "--splash=yes" ] ; then
    show_splash=true
  fi
done

SPLASH_ARG=""
if $show_splash ; then
    SPLASH_ARG="-splash:splash.gif"
fi

if [ `getconf LONG_BIT` = "64" ]; then
SCDIR=/usr/lib64/jitsi
else
SCDIR=/usr/lib/jitsi
fi

JITSI_COMMON_DIR=/usr/lib64/jitsi/sc-bundles
LIBPATH=$SCDIR/lib
CLASSPATH=$LIBPATH/felix.jar:$SCDIR/sc-bundles/dnsjava.jar:$SCDIR/sc-bundles/sc-launcher.jar:$JITSI_COMMON_DIR/util.jar:$LIBPATH
FELIX_CONFIG=$LIBPATH/felix.client.run.properties
LOG_CONFIG=$LIBPATH/logging.properties
COMMAND="$javabin $CLIENTARGS -classpath $CLASSPATH -Djna.library.path=$SCDIR/lib/native -Dfelix.config.properties=file:$FELIX_CONFIG -Djava.util.logging.config.file=$LOG_CONFIG $SPLASH_ARG -Dnet.java.sip.communicator.SC_HOME_DIR_NAME=.jitsi net.java.sip.communicator.launcher.SIPCommunicator"

# set add LIBPATH to LD_LIBRARY_PATH for any sc natives (e.g. jmf .so's)
export LD_LIBRARY_PATH="${LD_LIBRARY_PATH:+$LD_LIBRARY_PATH:}$SCDIR/lib/native"

cd $SCDIR

exec $COMMAND $*
