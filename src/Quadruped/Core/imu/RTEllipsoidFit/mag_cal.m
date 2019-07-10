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

%// Parts of this file are based on original code as below:

%******************************************************************************************
% Magnetometer Calibration Skript for Razor AHRS v1.4.2
% 9 Degree of Measurement Attitude and Heading Reference System
% for Sparkfun "9DOF Razor IMU" and "9DOF Sensor Stick"
%
% Released under GNU GPL (General Public License) v3.0
% Copyright (C) 2013 Peter Bartz [http://ptrbrtz.net]
% Copyright (C) 2012 Quality & Usability Lab, Deutsche Telekom Laboratories, TU Berlin
% Written by Peter Bartz (peter-bartz@gmx.de)
%
% Infos, updates, bug reports, contributions and feedback:
%     https://github.com/ptrbrtz/razor-9dof-ahrs
%******************************************************************************************

% mag_cal

% read in data from saved file

magFile = fopen('magRaw.dta', 'r');
magCalDataMat = fscanf(magFile, '%f %f %f', [3, inf]);
fprintf('Mat size = %d\n', size(magCalDataMat));
fclose(magFile);

% create the vectors

x = magCalDataMat(1, :)';
y = magCalDataMat(2, :)';
z = magCalDataMat(3, :)';

[center, radii, evecs, v] = ellipsoid_fit( [x y z ] );
fprintf('Center: %f %f %f\n', center(1), center(2), center(3));
fprintf('Radii: %f %f %f\n', radii(1), radii(2), radii(3));
fprintf('Evecs:\n%f %f %f\n%f %f %f\n%f %f %f\n', 
	evecs(1, 1), evecs(1, 2), evecs(1, 3),
	evecs(2, 1), evecs(2, 2), evecs(2, 3),
	evecs(3, 1), evecs(3, 2), evecs(3, 3));

scaleMat = inv([radii(1) 0 0; 0 radii(2) 0; 0 0 radii(3)]) * min(radii); 
correctionMat = evecs * scaleMat * evecs';

fprintf('correctionMat:\n%f %f %f\n%f %f %f\n%f %f %f\n', 
	correctionMat(1, 1), correctionMat(1, 2), correctionMat(1, 3),
	correctionMat(2, 1), correctionMat(2, 2), correctionMat(2, 3),
	correctionMat(3, 1), correctionMat(3, 2), correctionMat(3, 3));

	
% now correct the data to show that it works

magVector = [x - center(1), y - center(2), z - center(3)]';	% take off center offset
magVector = correctionMat * magVector;				% do rotation and scale
xCorr = magVector(1, :);					% get corrected vectors
yCorr = magVector(2, :);
zCorr = magVector(3, :);

mag_fit_display(x, y, z, center, radii, v, xCorr, yCorr, zCorr);
