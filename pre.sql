INSERT INTO `board_filetype` (`extension`,`mime`,`category_id`)
VALUES
	('jpg', 'image/jpeg', 1),
	('jpeg', 'image/jpeg', 1),
	('gif', 'image/gif', 1),
	('png', 'image/png', 1),
	('svg', 'image/svg', 1),
	('tiff', 'image/tiff', 1),
	('webp', 'image/webp', 1),
	('mp3', 'audio/mpeg', 2),
	('midi', 'audio/midi', 2),
	('ogg', 'audio/ogg', 2),
	('3gp', 'video/3gpp', 3),
	('mpg', 'video/mpeg', 3),
	('mpeg', 'video/mpeg', 3),
	('ogv', 'video/ogg', 3),
	('mov', 'video/quicktime', 3),
	('webm', 'videm/webm', 3),
	('flv', 'video/x-flv', 3),
	('wmv', 'video/x-ms-wmv', 3),
	('avi', 'video/x-msvideo', 3),
	('html', 'text/html', 4),
	('htm', 'text/html', 4),
	('doc', 'application/msword', 4),
	('docx', 'application/msword', 4),
	('pdf', 'application/pdf', 4),
	('txt', 'text/plain', 4),
	('swf', 'application/x-shockwave-flash', 6);

INSERT INTO `board_filecategory` (`name`)
VALUES
	('Изображения'),
	('Аудио'),
	('Видео'),
	('Текст'),
	('Архивы'),
	('Флеш');
