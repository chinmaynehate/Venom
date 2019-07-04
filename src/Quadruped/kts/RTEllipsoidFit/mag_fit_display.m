%//
%//  Copyright (c) 2014, richards-tech
%//	
%//  This file is part of RTEllipsoidFit
%//
%//  RTEllipsoidFit is free software: you can redistribute it and/or modify
%//  it under the terms of the GNU General Public License as published by
%//  the Free Software Foundation, either version 3 of the License, or
%//  (at your option) any later version.
%//
%//  RTEllipsoidFit is distributed in the hope that it will be useful,
%//  but WITHOUT ANY WARRANTY; without even the implied warranty of
%//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
%//  GNU General Public License for more details.
%//
%//  You should have received a copy of the GNU General Public License
%//  along with RTEllipsoidFit.  If not, see <http://www.gnu.org/licenses/>.
%//

function mag_fit_display(x, y, z, center, radii, v, xCorr, yCorr, zCorr)

displayRadius = 100;

figure(1);
hold on;

grid;
xlabel('x');
ylabel('y');
zlabel('z');
axis ([-displayRadius, displayRadius, -displayRadius, displayRadius, -displayRadius, displayRadius], "square");
title('Uncorrected samples (red) and corrected (blue) values');
plot3( x, y, z, ['.' 'r'] );
plot3( xCorr, yCorr, zCorr, ['.' 'b'] );

% display immediately

drawnow();

end
