def animate_piece_move(canvas, piece_tag, start_coords, end_coords, steps=20, delay=20):
    dx = (end_coords[0] - start_coords[0]) / steps
    dy = (end_coords[1] - start_coords[1]) / steps
    for _ in range(steps):
        canvas.move(piece_tag, dx, dy)
        canvas.update()
        canvas.after(delay)

def animate_piece_flash(canvas, piece_tag, flash_color="yellow", flashes=1, delay=500):
    original_color = canvas.itemcget(piece_tag, "fill")
    
    def toggle(count):
        if count > 0:
            current = canvas.itemcget(piece_tag, "fill")
            new_color = flash_color if current == original_color else original_color
            canvas.itemconfigure(piece_tag, fill=new_color)
            canvas.after(delay, lambda: toggle(count - 1))
        else:
            canvas.itemconfigure(piece_tag, fill=original_color)
    
    toggle(flashes * 2)
