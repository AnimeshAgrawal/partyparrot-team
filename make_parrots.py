from PIL import Image
import face_recognition, os 

supported_types = ('.png', '.jpg', '.jpeg', '.tiff')
inputs = []
for f in os.listdir('input'):
    if f.lower().endswith(supported_types):
        inputs.append(f)
    else:
        print('Ignored unsupported file ' + f)

if not os.path.isdir('parrots'):
    os.mkdir('parrots')

positions = [(124, 29), (88, 20), (61, 20), (16, 24), (16, 38), (34, 56), (70, 74), (115, 56), (133, 47), (142, 38)]

for input_file in inputs:
    raw_img = face_recognition.load_image_file(os.path.join('input', input_file))
    i = 1
    while i < 8:
        face_locations = face_recognition.face_locations(raw_img, number_of_times_to_upsample=i)
        if len(face_locations):
            break
    count = 0
    for face in face_locations:
        top, right, bottom, left = face
        face_arr = raw_img[top:bottom, left:right]
        face_img = Image.fromarray(face_arr).resize((150, 150), Image.LANCZOS)
        frames = []
        for i in range(10):
            parrot_frame = Image.open(os.path.join('.parrot_frames', str(i) + '.tiff'))
            alpha = parrot_frame.split()[3]
            parrot_frame.paste(face_img, positions[i])
            parrot_frame = parrot_frame.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
            mask = Image.eval(alpha, lambda a: 255 if a <=128 else 0)
            parrot_frame.paste(255, mask)
            frames.append(parrot_frame)
        if count > 0:
            name = input_file.split('.')[0] + str(count) + '.gif'
        else:
            name = input_file.split('.')[0] + '.gif'
        frames[0].save(os.path.join('parrots', name), 
            save_all=True, append_images=frames[1:], format="GIF", duration=40, transparency=255, disposal=2)
        count += 1
    print(input_file.split()[0] + ' has joined the party!')

