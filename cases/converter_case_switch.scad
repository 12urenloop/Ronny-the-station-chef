// this is the case for a XL9006-based adjustable buck/boost converter that powers the switch

board_x = 48+(15*2);
board_y = 26;
board_z = 15;

holes_x = 36;
holes_y = 18;

trimpot_x = 100;      //from center
trimpot_y = 7.5;

thickness = 2;
rfillet = 4;

dwires = 3.5;


int_x = board_x + 10;
$fn=64;


//---------------------


bottom();
translate([0, board_y + 10, 0]) top();


//---------------------


module bottom() 
{
    difference() {  
        union() {
            base();  
            
            //ziptie mounts
            difference() {
                union() {
                    translate([-int_x/2, -(dwires+1)/2, -board_z/2]) cube([4.5, dwires+1, board_z/2-dwires/2.5]);
                    translate([int_x/2-4.5, -(dwires+1)/2, -board_z/2]) cube([4.5, dwires+1, board_z/2-dwires/2.5]);
                }
                translate([-int_x/2, -(dwires+1)/2, -board_z/2+1]) cube([3.2, dwires+1, board_z/2-dwires/2-3]);
                translate([int_x/2-3.2, -(dwires+1)/2, -board_z/2+1]) cube([3.2, dwires+1, board_z/2-dwires/2-3]);
            }
        }

        
        wireholes();
        translate([0,0,board_z+2])cube([board_x*2, board_y*2, board_z*2], center = true);       

        difference() {
                translate([0,0,2])cube([board_x*2, board_y*2, 4], center = true);
                rcube([int_x + thickness, board_y + thickness, board_z + thickness], rfillet - thickness/2, center = true);  
        }          
            
    }
    
    //board mounts
    translate([-holes_x/2, holes_y/2, -board_z/2]) cylinder(d = 5, h = 1);
    translate([holes_x/2, -holes_y/2, -board_z/2]) cylinder(d = 5, h = 1);
    translate([holes_x/2, holes_y/2, -board_z/2]) cylinder(d = 5, h = 1);
    translate([-holes_x/2, -holes_y/2, -board_z/2]) cylinder(d = 5, h = 1);    
    translate([-holes_x/2, holes_y/2, -board_z/2]) cylinder(d = 2.2, h = 4);
    translate([holes_x/2, -holes_y/2, -board_z/2]) cylinder(d = 2.2, h = 4);
}



module top() 
{
    difference() {    
        base();
        wireholes();
        translate([0,0,board_z])cube([board_x*2, board_y*2, board_z*2], center = true);    
        intersection() {
            rcube([int_x + thickness, board_y + thickness, board_z + thickness], rfillet - thickness/2, center = true);
            translate([0,0,0])cube([board_x*2, board_y*2, 4], center = true);
        }
        
        translate([trimpot_x, -trimpot_y, -board_z/2-thickness]) cylinder(d = 3.5 , h = thickness+1);
    }
}



module base () 
{
    difference() {
        rcube([int_x + thickness*2, board_y + thickness*2, board_z + thickness*2], rfillet, center = true);
        rcube([int_x, board_y, board_z], rfillet-thickness, center = true);

    }
}


module wireholes() 
{
    hull() {
        rotate([0, 90, 0]) cylinder(d = dwires, h = int_x+thickness*2, center = true);  
        translate([0,0,4]) rotate([0, 90, 0]) cylinder(d = dwires, h = board_x+rfillet*2+thickness*2, center= true); 
    }
    
    hull() {
        translate([int_x/2+thickness,0,0]) rotate([0, 90, 0]) cylinder(d1 = dwires, d2 = dwires+2, h = thickness*0.5, center = true);  
        translate([int_x/2+thickness,0,4]) rotate([0, 90, 0]) cylinder(d1 = dwires, d2 = dwires+2, h = thickness*0.5, center= true); 
    }
    hull() {
        translate([-int_x/2-thickness,0,0]) rotate([0, 90, 0]) cylinder(d2 = dwires, d1 = dwires+2, h = thickness*0.5, center = true);  
        translate([-int_x/2-thickness,0,4]) rotate([0, 90, 0]) cylinder(d2 = dwires, d1 = dwires+2, h = thickness*0.5, center= true); 
    }
}



module rcube (size, rfillet=1, center=false) 
{ 
    sx = size[0] - rfillet*2;
    sy = size[1] - rfillet*2;
    sz = size[2] - rfillet*2;
    
    tx = center ? -size[0]/2 + rfillet : rfillet;
    ty = center ? -size[1]/2 + rfillet : rfillet;
    tz = center ? -size[2]/2 + rfillet : rfillet;

    translate([tx, ty, tz]) hull() {        
        translate([ 0, 0, 0 ]) sphere (r = rfillet);
        translate([sx, 0, 0 ]) sphere (r = rfillet);
        translate([ 0,sy, 0 ]) sphere (r = rfillet);
        translate([sx,sy, 0 ]) sphere (r = rfillet);
        translate([ 0, 0,sz ]) sphere (r = rfillet);
        translate([sx, 0,sz ]) sphere (r = rfillet);   
        translate([ 0,sy,sz ]) sphere (r = rfillet);
        translate([sx,sy,sz ]) sphere (r = rfillet);                
    }
}