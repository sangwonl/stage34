var path = require('path');
var fs = require('fs');
var _root = path.resolve(__dirname, '..');

function root(args) {
    args = Array.prototype.slice.call(arguments, 0);
    return path.join.apply(path, [_root].concat(args));
}

function fileExists(filePath, cb) {
    return fs.existsSync(filePath);
}

exports.root = root;
exports.fileExists = fileExists;
