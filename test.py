from pywinauto import Desktop

desktop = Desktop(backend="win32")

print("\n========== ALL PRINT WINDOWS ==========\n")

for w in desktop.windows(title="Print:", visible_only=True):

    print("WINDOW")
    print("Handle:", w.handle)
    print("Title:", repr(w.window_text()))
    print("Class:", w.class_name())

    print("\n--- BUTTONS ---")

    for i, control in enumerate(w.descendants(class_name="Button")):

        try:
            print(
                f"[{i}] "
                f"text={control.window_text()!r} "
                f"class={control.class_name()!r} "
                f"handle={control.handle}"
            )
        except Exception:
            pass

    print("\n")


print("\n========== ERROR WINDOWS ==========\n")

for w in desktop.windows(
    class_name="#32770",
    visible_only=True
):

    try:

        print("WINDOW")
        print("Handle:", w.handle)
        print("Title:", repr(w.window_text()))
        print("Class:", w.class_name())

        print("\n--- ALL CONTROLS ---")

        for i, control in enumerate(w.descendants()):

            try:
                text = control.window_text()

                if text.strip():
                    print(
                        f"[{i}] "
                        f"text={text!r} "
                        f"class={control.class_name()!r} "
                        f"handle={control.handle}"
                    )

            except Exception:
                pass

        print("\n-----------------------------\n")

    except Exception:
        pass
