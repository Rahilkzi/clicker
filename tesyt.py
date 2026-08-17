from pywinauto import Desktop
import time


# ============================================================
# SAP PRINT BUTTON TEST
# ============================================================

desktop = Desktop(backend="win32")

print()
print("=" * 60)
print("              SAP PRINT BUTTON TEST")
print("=" * 60)


# ------------------------------------------------------------
# Find SAP Print window
# ------------------------------------------------------------

print_window = None

for w in desktop.windows(
    title="Print:",
    class_name="#32770",
    visible_only=True
):
    print_window = w
    break


if print_window is None:
    print("\n❌ SAP Print window not found.")
    print("Open the SAP Print window and run the script again.")
    exit()


print("\n✓ Print window found")
print("Handle :", print_window.handle)
print("Title  :", repr(print_window.window_text()))
print("Class  :", print_window.class_name())


# ------------------------------------------------------------
# Find buttons
# ------------------------------------------------------------

buttons = print_window.descendants(class_name="Button")

print()
print(f"Buttons found: {len(buttons)}")
print()


for i, button in enumerate(buttons):

    try:
        rect = button.rectangle()

        print(
            f"[{i}] "
            f"Class={button.class_name()} "
            f"Text={button.window_text()!r} "
            f"Handle={button.handle} "
            f"Position=({rect.left},{rect.top}) "
            f"Size=({rect.width()},{rect.height()})"
        )

    except Exception as e:
        print(f"[{i}] ERROR: {e}")


# ------------------------------------------------------------
# Identify Print button
#
# From your screenshot:
#
# Button 0 -> position around (62,200), size 0x0
# Button 1 -> position around (403,619), size 59x20
# Button 2 -> position around (463,619), size 59x20
# Button 3 -> position around (522,619), size 20x20
#
# Therefore Button 1 is the PRINT button.
# ------------------------------------------------------------

print_button = None

for button in buttons:

    try:
        rect = button.rectangle()

        # Ignore invisible/zero-size buttons
        if rect.width() < 30 or rect.height() < 15:
            continue

        # Print button is the first sizeable button in this area.
        if rect.left >= 350 and rect.top >= 550:
            print_button = button
            break

    except Exception:
        pass


if print_button is None:

    print()
    print("❌ PRINT BUTTON NOT FOUND")
    exit()


print()
print("=" * 60)
print("PRINT BUTTON FOUND")
print("=" * 60)

print("Handle :", print_button.handle)
print("Class  :", print_button.class_name())
print("Text   :", repr(print_button.window_text()))

try:
    rect = print_button.rectangle()

    print(
        "Position:",
        f"({rect.left},{rect.top})"
    )

    print(
        "Size:",
        f"({rect.width()},{rect.height()})"
    )

except Exception:
    pass


# ------------------------------------------------------------
# Wait for user
# ------------------------------------------------------------

input("\nPress ENTER to click the PRINT button...")


# ------------------------------------------------------------
# Click PRINT
# ------------------------------------------------------------

try:

    print("\nClicking PRINT button...")

    # IMPORTANT:
    # Do NOT use child_window().
    # This is already the Button wrapper.
    print_button.click()

    print("✓ PRINT button clicked successfully.")

except Exception as e:

    print("❌ Could not click PRINT button.")
    print("Error:", e)
    exit()


# ------------------------------------------------------------
# Wait for possible PDF error dialog
# ------------------------------------------------------------

print()
print("Waiting for possible PDF error window...")

time.sleep(1)


# ------------------------------------------------------------
# Search for PDF error dialog
# ------------------------------------------------------------

error_window = None

for w in desktop.windows(
    class_name="#32770",
    visible_only=True
):

    try:

        title = w.window_text()

        # The error window title contains the PDF path,
        # for example:
        #
        # C:\temp\0999324283.pdf
        #
        if ".pdf" in title.lower():

            error_window = w
            break

    except Exception:
        pass


# ------------------------------------------------------------
# Handle error dialog
# ------------------------------------------------------------

if error_window is not None:

    print()
    print("=" * 60)
    print("⚠ PDF ERROR WINDOW DETECTED")
    print("=" * 60)

    print("Title :", repr(error_window.window_text()))
    print("Handle:", error_window.handle)

    # Find OK button directly
    ok_button = None

    for button in error_window.descendants(class_name="Button"):

        try:

            if button.window_text().strip().upper() == "OK":

                ok_button = button
                break

        except Exception:
            pass


    if ok_button is not None:

        print("✓ OK button found")

        try:

            ok_button.click()

            print("✓ Error window closed.")

        except Exception as e:

            print("❌ Could not click OK.")
            print("Error:", e)

    else:

        print("❌ OK button not found.")


else:

    print()
    print("✓ No PDF error window detected.")


# ------------------------------------------------------------
# Finished
# ------------------------------------------------------------

print()
print("=" * 60)
print("TEST FINISHED")
print("=" * 60)