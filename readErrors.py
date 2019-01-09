import IP 

if __name__=="__main__":
    while True:
        angle,transLation,x1,x2,y1,y2  = IP.getSlopeError()
        print("Angle:",angle,"Lateral Error:",transLation)
        print("x1:",x1," , x2:",x2," , y1:",y1," , y2:",y2)