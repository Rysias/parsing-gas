import src.extract as extract
from io import BytesIO


def test_parse_xml_tags():
    xml = BytesIO(
        b"""\
            <root>
    <RandomObject>
        <byg406Koordinatsystem> lol </byg406Koordinatsystem>
    </RandomObject>
    <Bygning>
        <unimportant> ignore me </unimportant>
        <parseMe>parse me</parseMe> 
    </Bygning>
    </root>
    """
    )
    target_tags = ["parseMe"]
    target_obj = "Bygning"
    assert next(
        extract.get_target_tags(
            xml, target_tags=target_tags, target_obj=target_obj, stop_tag="root"
        )
    ) == {"parseMe": "parse me"}


def test_parse_two_tags():
    xml = BytesIO(
        b"""\
            <root>
    <RandomObject>
        <byg406Koordinatsystem> lol </byg406Koordinatsystem>
    </RandomObject>
    <Bygning>
        <unimportant> ignore me </unimportant>
        <parseMe>parse me</parseMe> 
        <alsoParseMe>also parse me</alsoParseMe>
    </Bygning>
    </root>
    """
    )
    target_tags = ["parseMe", "alsoParseMe"]
    target_obj = "Bygning"
    assert next(
        extract.get_target_tags(
            xml, target_tags=target_tags, target_obj=target_obj, stop_tag="root"
        )
    ) == {"parseMe": "parse me", "alsoParseMe": "also parse me"}


def test_parse_two_objs():
    xml = BytesIO(
        b"""\
            <root>
    <RandomObject>
        <byg406Koordinatsystem> lol </byg406Koordinatsystem>
    </RandomObject>
    <Bygning>
        <unimportant> ignore me </unimportant>
        <parseMe>parse me</parseMe> 
        <alsoParseMe>also parse me</alsoParseMe>
    </Bygning>
    <Bygning>
        <parseMe>parse me</parseMe> 
    </Bygning>
    </root>
    """
    )
    target_tags = ["parseMe", "alsoParseMe"]
    target_obj = "Bygning"
    assert list(
        extract.get_target_tags(
            xml, target_tags=target_tags, target_obj=target_obj, stop_tag="root"
        )
    ) == [
        {"parseMe": "parse me", "alsoParseMe": "also parse me"},
        {"parseMe": "parse me"},
    ]


def test_stop_tag():
    xml = BytesIO(
        b"""\
            <root>
    <BygningList>
        <Bygning>
            <parseMe>parse me</parseMe> 
            <alsoParseMe>also parse me</alsoParseMe>
        </Bygning>
        <Bygning>
            <parseMe>parse me</parseMe> 
        </Bygning>
    </BygningList>
    <Bygning>
        <parseMe>This should not be there</parseMe>
    </Bygning>
    </root>
    """
    )
    target_tags = ["parseMe", "alsoParseMe"]
    target_obj = "Bygning"
    stop_tag = "BygningList"
    assert list(
        extract.get_target_tags(
            xml, target_tags=target_tags, target_obj=target_obj, stop_tag=stop_tag
        )
    ) == [
        {"parseMe": "parse me", "alsoParseMe": "also parse me"},
        {"parseMe": "parse me"},
    ]
