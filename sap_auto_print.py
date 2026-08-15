from pywinauto import Desktop
import time


ERROR_TEXT = "This file does not have an app associated with it"

running = True


def find_print_window():
    """
    Find the SAP Print dialog.
    """
    try:
        windows = Desktop(backend="win32").windows(
            title_re=r"^Print:$",
            visible_only=True
        )

        for window in windows:
            try:
                if "saplogon.exe" in window.process_module():
                    return window
            except Exception:
                return window

    except Exception:
        pass

    return None


def find_error_window():
    """
    Find the Windows PDF association error.
    """

    try:
        windows = Desktop(backend="win32").windows(
            class_name="#32770",
            visible_only=True
        )

        for window in windows:

            try:
                text = window.window_text()

                # Check all controls inside the dialog
                for control in window.descendants():
                    try:
                        text += " " + control.window_text()
                    except Exception:
                        pass

                if ERROR_TEXT in text:
                    return window

            except Exception:
                continue

    except Exception:
        pass

    return None


def click_print(window):
    """
    Click SAP's Button3 = Print.
    """

    try:
        button = window.child_window(
            class_name="Button",
            found_index=2
        )

        print("Clicking Print...")
        button.click()

        return True

    except Exception as e:
        print("Print button error:", e)
        return False


def press_error_ok(window):
    """
    Click Button1 = OK.
    """

    try:
        ok_button = window.child_window(
            title="OK",
            class_name="Button"
        )

        print("Error detected → pressing OK")

        # .click() sends the control command rather than
        # physically moving the mouse.
        ok_button.click()

        return True

    except Exception as e:
        print("OK button error:", e)

        # Fallback: send Enter to the dialog
        try:
            window.set_focus()
            window.type_keys("{ENTER}")
            return True
        except Exception:
            return False


print("====================================")
print(" SAP AUTO PRINT")
print("====================================")
print()
print("F8 / Ctrl+C to stop")
print()


# ----------------------------------------------------------
# MAIN LOOP
# ----------------------------------------------------------

while running:

    try:

        # ==================================================
        # 1. ERROR HAS HIGHEST PRIORITY
        # ==================================================

        error_window = find_error_window()

        if error_window:

            press_error_ok(error_window)

            # Wait until error disappears
            for _ in range(30):

                time.sleep(0.2)

                if not find_error_window():
                    break

            continue


        # ==================================================
        # 2. LOOK FOR SAP PRINT WINDOW
        # ==================================================

        print_window = find_print_window()

        if print_window:

            print("Print window detected")

            # Click Print ONCE
            click_print(print_window)

            # IMPORTANT:
            # Don't immediately click again.
            #
            # Wait for SAP to close the Print window.
            for _ in range(50):

                time.sleep(0.2)

                if not find_print_window():
                    break

            # Give SAP a moment to generate/open PDF
            time.sleep(0.5)

            continue


        # ==================================================
        # 3. NOTHING TO DO
        # ==================================================

        time.sleep(0.2)


    except KeyboardInterrupt:

        print()
        print("Stopped by user.")
        break

    except Exception as e:

        print("Unexpected error:", e)
        time.sleep(1)