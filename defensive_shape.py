"""A compact back four with three midfielders, positioned before the shot target."""

def block(ball_x,ball_y):
    centre=max(-8.5,min(8.5,ball_x*.45))
    depth=max(4.8,min(12.,ball_y*.43));spacing=7.
    back=[(centre+x,depth+.25*abs(x)/10.5,'defence')for x in (-10.5,-3.5,3.5,10.5)]
    midfield=[(centre+x,depth+4.8,'midfield')for x in (-spacing,0.,spacing)]
    positions=back+midfield
    if min((x-ball_x)**2+(y-ball_y)**2 for x,y,_ in positions)<1.8**2:
        candidates=(-2.,2.)
        offset=max(candidates,key=lambda dx:min((x+dx-ball_x)**2+(y-ball_y)**2 for x,y,_ in positions))
        positions=[(x+offset,y,line)for x,y,line in positions]
    return tuple(positions)

def shift(delivery,progress):
    p=max(0.,min(1.,progress));remaining=1-p*p*(3-2*p)
    start,end=delivery.points[0],delivery.contact
    a=max(-8.5,min(8.5,start[0]*.45));b=max(-8.5,min(8.5,end[0]*.45))
    return (a-b)*remaining,min(1.5,max(0.,(start[1]-end[1])*.08))*remaining
