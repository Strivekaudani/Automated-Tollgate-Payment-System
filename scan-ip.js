
const child_process = require('child_process');

console.clear();


let i = 0;
function scanIP() {

	if (i === 256)
		return;

	const ip = `10.42.0.${i}`

	child_process.exec(`ping -c 2 ${ip}`, function(err, stdout, stderr) {

		if (err) {
			// console.error('CMD_ERROR', err.toString())
		} else if (stderr) {
			// console.error(stderr)
		} else {
			console.log('IP FOUND:', ip)
		}

		i++;
		scanIP()

	})

}

scanIP()