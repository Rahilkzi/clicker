from pywinauto import Desktop


ERROR_TEXT = "This file does not have an app associated with it"

desktop = Desktop(backend="win32")


print()
print("=" * 60)
print("              SAP UI AUTOMATION TEST")
print("=" * 60)


# ============================================================
# FIND SAP PRINT WINDOWS
# ============================================================

print()
print("========== SAP PRINT WINDOWS ==========")
print()

print_windows = []

for window in desktop.windows(visible_only=True):

    try:
        title = window.window_text().strip()

        if title == "Print:":

            print_windows.append(window)

            print("WINDOW")
            print("Title  :", repr(title))
            print("Class  :", window.class_name())
            print("Handle :", window.handle)
            print("PID    :", window.element_info.process_id)

            print()
            print("--- BUTTONS ---")

            for i, button in enumerate(
                window.descendants(class_name="Button")
            ):

                try:
                    print(
                        f"[{i}] "
                        f"text={button.window_text()!r} "
                        f"class={button.class_name()!r} "
                        f"handle={button.handle}"
                    )
                except Exception:
                    pass

            print()
            print("-" * 60)

    except Exception:
        pass


if print_windows:
    print()
    print("✓ SAP Print window FOUND")
else:
    print()
    print("❌ SAP Print window NOT FOUND")


# ============================================================
# FIND WINDOWS ERROR DIALOGS
# ============================================================

print()
print("========== WINDOWS ERROR DIALOGS ==========")
print()


error_windows = []

dialogs = desktop.windows(
    class_name="#32770",
    visible_only=True
)


print("Total #32770 dialogs found:", len(dialogs))
print()


for number, dialog in enumerate(dialogs, start=1):

    try:

        title = dialog.window_text().strip()

        print("=" * 60)
        print("DIALOG #", number)
        print("=" * 60)

        print("Title  :", repr(title))
        print("Class  :", repr(dialog.class_name()))
        print("Handle :", dialog.handle)

        try:
            print(
                "PID    :",
                dialog.element_info.process_id
            )
        except Exception:
            pass

        print()
        print("--- CONTROLS ---")

        found_error = False

        for i, control in enumerate(dialog.descendants()):

            try:

                text = control.window_text().strip()

                if not text:
                    continue

                print(
                    f"[{i}] "
                    f"text={text!r} "
                    f"class={control.class_name()!r} "
                    f"handle={control.handle}"
                )

                if ERROR_TEXT.lower() in text.lower():
                    found_error = True

            except Exception:
                pass


        # Check dialog title too

        if ERROR_TEXT.lower() in title.lower():
            found_error = True


        if found_error:

            error_windows.append(dialog)

            print()
            print(">>> PDF ERROR WINDOW FOUND <<<")
            print()

        else:

            print()
            print("Not the PDF error dialog.")
            print()


    except Exception as e:

        print("Dialog inspection error:", e)


# ============================================================
# FINAL SUMMARY
# ============================================================

print()
print("=" * 60)
print("                    TEST SUMMARY")
print("=" * 60)
print()


if print_windows:
    print("SAP Print window : FOUND")
else:
    print("SAP Print window : NOT FOUND")


if error_windows:
    print(
        "PDF Error window : FOUND"
        f" ({len(error_windows)})"
    )
else:
    print("PDF Error window : NOT FOUND")


print()
print("=" * 60)
