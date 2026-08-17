import time
from pywinauto import Desktop


# ============================================================
# SAP AUTO PRINT
# ============================================================

desktop = Desktop(backend="win32")

CHECK_INTERVAL = 0.2
PRINT_WAIT_TIMEOUT = 15


print()
print("=" * 60)
print("                 SAP AUTO PRINT")
print("=" * 60)
print()
print("F8 / Ctrl+C to stop")
print()


# ============================================================
# FIND SAP PRINT WINDOW
# ============================================================

def get_print_windows():

    result = []

    try:

        windows = desktop.windows(
            title="Print:",
            class_name="#32770",
            visible_only=True
        )

        for window in windows:

            try:

                if window.is_visible():
                    result.append(window)

            except Exception:
                pass

    except Exception:
        pass

    return result


# ============================================================
# FIND PDF ERROR WINDOW
# ============================================================

def get_pdf_error_windows():

    result = []

    try:

        dialogs = desktop.windows(
            class_name="#32770",
            visible_only=True
        )

    except Exception:
        return result


    for dialog in dialogs:

        try:

            title = dialog.window_text().strip()

            # ------------------------------------------------
            # PDF error dialog identification
            #
            # Example:
            #
            # C:\temp\0999324283.pdf
            # ------------------------------------------------

            if not title.lower().endswith(".pdf"):
                continue


            # ------------------------------------------------
            # Make sure an OK button exists
            # ------------------------------------------------

            ok_button = None

            try:

                buttons = dialog.descendants(
                    class_name="Button"
                )

                for button in buttons:

                    try:

                        text = button.window_text().strip()

                        if text.upper() == "OK":

                            ok_button = button
                            break

                    except Exception:
                        pass

            except Exception:
                pass


            if ok_button is not None:

                result.append(
                    (dialog, ok_button)
                )

        except Exception:
            pass


    return result


# ============================================================
# CLICK PRINT BUTTON
# ============================================================

def click_print(print_window):

    try:

        # ----------------------------------------------------
        # From your Window Spy:
        #
        # Print button = Button3
        #
        # pywinauto's descendant index corresponds to it.
        # ----------------------------------------------------

        buttons = print_window.descendants(
            class_name="Button"
        )


        print(
            f"Found {len(buttons)} buttons in Print window"
        )


        # ----------------------------------------------------
        # Button3 = index 3
        # ----------------------------------------------------

        if len(buttons) >= 4:

            print_button = buttons[3]

            print(
                "Print button handle:",
                print_button.handle
            )

            print("Clicking PRINT...")

            # Windows control click.
            # Does NOT move the mouse cursor.
            print_button.click()

            return True


        print(
            "❌ Print button could not be identified."
        )

        return False


    except Exception as e:

        print(
            "❌ Print button error:",
            repr(e)
        )

        return False


# ============================================================
# PRESS ERROR OK
# ============================================================

def close_pdf_error(dialog, ok_button):

    try:

        print()
        print("========================================")
        print("PDF ERROR DETECTED")
        print("========================================")

        print(
            "PDF dialog:",
            repr(dialog.window_text())
        )

        print(
            "OK handle:",
            ok_button.handle
        )

        print("Pressing OK...")

        # Windows control click.
        # Does NOT move the mouse.
        ok_button.click()

        print("✓ Error dialog closed")

        return True

    except Exception as e:

        print(
            "❌ Error closing PDF dialog:",
            repr(e)
        )

        return False


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    try:

        # ----------------------------------------------------
        # 1. CHECK FOR PDF ERROR FIRST
        # ----------------------------------------------------

        errors = get_pdf_error_windows()


        if errors:

            for dialog, ok_button in errors:

                close_pdf_error(
                    dialog,
                    ok_button
                )

            time.sleep(0.5)

            continue


        # ----------------------------------------------------
        # 2. FIND PRINT WINDOW
        # ----------------------------------------------------

        print_windows = get_print_windows()


        if not print_windows:

            time.sleep(
                CHECK_INTERVAL
            )

            continue


        # ----------------------------------------------------
        # 3. PRINT WINDOW FOUND
        # ----------------------------------------------------

        print()
        print("========================================")
        print("PRINT WINDOW DETECTED")
        print("========================================")

        print(
            "Number of Print windows:",
            len(print_windows)
        )


        # ----------------------------------------------------
        # Use the first visible Print window
        # ----------------------------------------------------

        print_window = print_windows[0]


        print(
            "Handle:",
            print_window.handle
        )

        print(
            "PID:",
            print_window.element_info.process_id
        )


        # ----------------------------------------------------
        # 4. CLICK PRINT
        # ----------------------------------------------------

        clicked = click_print(
            print_window
        )


        if not clicked:

            print(
                "Waiting for Print window..."
            )

            time.sleep(1)

            continue


        # ----------------------------------------------------
        # 5. AFTER PRINT CLICK
        #
        # Wait for either:
        #
        # A) PDF error appears
        #
        # OR
        #
        # B) Print window disappears
        # ----------------------------------------------------

        start_time = time.time()


        while (
            time.time() - start_time
            < PRINT_WAIT_TIMEOUT
        ):

            # -----------------------------------------------
            # Check PDF error
            # -----------------------------------------------

            errors = get_pdf_error_windows()


            if errors:

                for dialog, ok_button in errors:

                    close_pdf_error(
                        dialog,
                        ok_button
                    )

                break


            # -----------------------------------------------
            # Check whether Print window still exists
            # -----------------------------------------------

            current_print_windows = (
                get_print_windows()
            )


            if not current_print_windows:

                print()
                print(
                    "✓ Print window closed."
                )

                break


            time.sleep(
                CHECK_INTERVAL
            )


        # ----------------------------------------------------
        # Small delay before checking for next SAP item
        # ----------------------------------------------------

        time.sleep(0.5)


    except KeyboardInterrupt:

        print()
        print()
        print("=" * 60)
        print("SAP AUTO PRINT STOPPED")
        print("=" * 60)

        break


    except Exception as e:

        print()
        print(
            "Main loop error:",
            repr(e)
        )

        time.sleep(1)