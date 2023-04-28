import { __ } from 'i18n';
import { html } from 'lit';

export default () => {

    return html` <form class="sendXMPPMessage" id="correct-form">
        <label for="fname">Display message:</label><br />
        <code class="crr-input crr-display"></code>
        <br />
        <label for="lname">Corrected message:</label>
        <br />
        <textarea
            rows="4"
            class="crr-input crr-msg"
            type="text"
            id="correction-input"
            name="lname"
            placeholder="Enter your correction here..."
        ></textarea>
        <button type="submit" class="correct-button" form="correct-form" value="Submit">Submit</button>

        <converse-icon class="fas fa-times" color="var(--grey)" size="1em" id="close"></converse-icon>
    </form>`;
};
