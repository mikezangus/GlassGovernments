export default function ContactComponent(
    {
        phoneNumber,
        setPhoneNumber
    }:
    {
        phoneNumber: string;
        setPhoneNumber: (phoneNumber: string) => void;
    }
)
{
    return (
        <div>
            <input
                type="tel"
                placeholder="enter your phone number"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
            />
        </div>
    );
}