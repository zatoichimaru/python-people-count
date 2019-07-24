import datetime
import math
import cv2
import sys
import numpy as np

def foreheadIntersection( y, coordinateLineInputY, coordinateExitLineY ):
    absoluteDifference = abs( y - coordinateLineInputY )	

    if ( ( absoluteDifference <= 2 ) and ( y < coordinateExitLineY ) ):
        return 1
    else:
        return 0

def foreheadIntersectionExit( y, coordinateLineInputY, coordinateExitLineY ):
    absoluteDifference = abs( y - coordinateExitLineY )	

    if ( ( absoluteDifference <= 2 ) and ( y > coordinateLineInputY ) ):
        return 1
    else:
        return 0

def execute():
    width = 0
    height = 0
    counterEntries = 0
    exitsCounter = 0
    areaOutlineMinimumLimit = 3000
    thresholdBinary = 70
    offsetLineReference = 150
    firstFrame = None
    amountContours = 0

    cam = cv2.VideoCapture(0)

    #resolucao 640x480
    cam.set( 3,640 )
    cam.set( 4,480 )

    for i in range( 0,19 ):
        ( grabbed, frame ) = cam.read()

    while( cam.isOpened() ):
        ( grabbed, frame ) = cam.read()
        height = np.size( frame, 0 )
        width = np.size( frame, 1 )

        if not grabbed:
            break

        frameGray = cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY )
        frameGray = cv2.GaussianBlur( frameGray, ( 21, 21 ), 0 )

        if firstFrame is None:
            firstFrame = frameGray
            continue

        frameDelta = cv2.absdiff( firstFrame, frameGray )
        frameThresh = cv2.threshold( frameDelta, thresholdBinary, 255, cv2.THRESH_BINARY )[1]
        frameThresh = cv2.dilate( frameThresh, None, iterations=2 )
        allContour, _ = cv2.findContours( frameThresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        coordinateLineInputY = int( ( height / 2 ) - offsetLineReference )
        coordinateExitLineY = int( ( height / 2 ) + offsetLineReference )

        cv2.line(frame, ( 0,coordinateLineInputY) , ( width,coordinateLineInputY), ( 255, 0, 0 ), 2 )
        cv2.line(frame, ( 0,coordinateExitLineY ), ( width,coordinateExitLineY), ( 0, 0, 255 ), 2 )

        for contourValue in allContour:
            if cv2.contourArea( contourValue ) < areaOutlineMinimumLimit:
                continue

            amountContours += 1

            ( x, y, w, h ) = cv2.boundingRect( contourValue )

            coordinateContourCenterX = ( x + x + w ) / 2
            coordinateContourCenterY = ( y + y + h ) / 2
            centerPointOutline = ( int( coordinateContourCenterX ), int( coordinateContourCenterY ) )
  
            if ( foreheadIntersection( coordinateContourCenterY, coordinateLineInputY, coordinateExitLineY ) ):
                counterEntries += 1

            if ( foreheadIntersectionExit( coordinateContourCenterY, coordinateLineInputY, coordinateExitLineY ) ):  
                exitsCounter += 1

        #print("Contornos encontrados: "+str(amountContours))

        cv2.putText( frame, "Entradas1: {}" . format( str( counterEntries ) ), ( 10, 50 ),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 250, 0, 1 ), 1, cv2.LINE_AA )
        cv2.putText( frame, "Entradas2: {}" . format( str( exitsCounter ) ), ( 10, 70 ),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 1, cv2.LINE_AA )
        cv2.imshow( "Original", frame )
        cv2.waitKey( 1 )

    cam.release()
    cv2.destroyAllWindows()

def main():
    execute()

if __name__ == "__main__":
    main()