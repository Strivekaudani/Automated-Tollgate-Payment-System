

"use strict"

// "IF A FILE IS RENAMED, IT PRODUCES AN ERRROR, I SHOULD FIX THAT"

const FileWatcher = require('filewatcher');
const child = require('child_process');
const fs = require('fs');

const PI_IP = '10.42.0.20';


const fileWatcher = new FileWatcher();
const dirWatcher = new FileWatcher();

// recursively
function watchRecursively(root, name) {

	const path = `${root}/${name}`;

	const isDir = fs.lstatSync(path).isDirectory();

	if (isDir) {
		const contents = fs.readdirSync(path);
		contents.forEach(item => {
			watchRecursively(path, item);
		});
	} else {
		fileWatcher.add(path);
	}

}

const cuttingIndex = `${__dirname}/FLASK_APP`.length + 1;

fileWatcher.on('change', function(file, stat) {

	changingFile = file;

	console.log(file, 'CHANGED');

	const fileCutPath = file.substring(cuttingIndex);
	const cmd = `sshpass -p "raspberry" scp ${file} pi@${PI_IP}:/home/pi/clayton/FLASK_APP/${fileCutPath}`;

	child.exec(cmd, function (err, stdout, stderr) {
		
		if (err)
			console.log(err);

		if (stdout)
			console.log(stdout);

		if (stderr)
			console.log(stderr);

	});

})

console.clear();

let changingFile = null;

dirWatcher.add(__dirname + '/FLASK_APP');
dirWatcher.on('change', function(file, stats) {
	// when a new file is added, relisten for each file

	setTimeout(function() {

		if (changingFile) {
			changingFile = null;
			return;
		}

		console.log('REWATCHING...');
		fileWatcher.removeAll();
		watchRecursively(__dirname, 'FLASK_APP');

	}, 4000);

})

watchRecursively(__dirname, 'FLASK_APP');

console.log('WATCHING EVERYTHING ...');