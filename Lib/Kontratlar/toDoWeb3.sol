//SPDX-License-Identifier: Unlicense

pragma solidity 0.5.0;

contract toDoWeb3 {
    address public kurucu_cuzdan;
    uint256 public gorev_sayisi = 0;

    struct Gorev {
        address cuzdan;
        uint256 gorev_id;
        string icerik;
        bool tamamlanma;
    }

    mapping(uint256 => Gorev) public gorevler;

    event GorevOlustur(uint256 gorev_id, string icerik, bool tamamlanma);
    event GorevTamamla(uint256 gorev_id, bool tamamlanma);

    constructor() public {
        kurucu_cuzdan = msg.sender;
        gorevOlustur("toDoWeb3 Ayakta Kanka");
    }

    function gorevOlustur(string memory _gorev_id) public {
        gorev_sayisi++;
        gorevler[gorev_sayisi] = Gorev(msg.sender, gorev_sayisi, _gorev_id, false);
        emit GorevOlustur(gorev_sayisi, _gorev_id, false);
    }

    function gorevTamamla(uint256 _gorev_id) public {
        Gorev memory _gorev = gorevler[_gorev_id];

        require(_gorev.cuzdan == msg.sender);

        _gorev.tamamlanma = !_gorev.tamamlanma;
        gorevler[_gorev_id] = _gorev;
        emit GorevTamamla(_gorev_id, _gorev.tamamlanma);
    }
}